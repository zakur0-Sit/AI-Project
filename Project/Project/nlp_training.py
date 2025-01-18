import spacy
import json
from collections import Counter

# Load the constraints from the JSON file
with open('constraints.json', 'r') as file:
    constraints_data = json.load(file)

# Extract professor constraints and student constraints
professor_constraints = constraints_data.get('professor_constraints', [])
student_constraints = constraints_data.get('student_constraints', [])

# Load the trained model for extracting entities (modify model path as needed)
model_path = "unavailability_model"  # Change to your model's saved path
nlp = spacy.load(model_path)

# Map plural days to their singular form
plural_to_singular = {
    "Mondays": "Monday",
    "Tuesdays": "Tuesday",
    "Wednesdays": "Wednesday",
    "Thursdays": "Thursday",
    "Fridays": "Friday",
    "Saturdays": "Saturday",
    "Sundays": "Sunday"
}


# Function to handle singular/plural mapping
def map_plural_to_singular(day):
    return plural_to_singular.get(day, day)


# Helper function to convert time descriptions like 'before 2 PM' to a range
def convert_time_range_to_start_end(time_range):
    time_mapping = {
        "before 2 PM": "08:00-14:00",
        "before 3 PM": "08:00-15:00",
        "before 4 PM": "08:00-16:00",
        "before 5 PM": "08:00-17:00",
        "before 6 PM": "08:00-18:00",
        "before 7 PM": "08:00-19:00",
        "before 8 PM": "08:00-20:00",
        "afternoons": "12:00-16:00",
        "mornings": "08:00-12:00",
        "evenings": "16:00-20:00",
    }
    return time_mapping.get(time_range.lower(), "08:00-20:00")  # Default time if not found


# Function to extract entities from the text using the model
def extract_constraints(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]


# Function to map extracted entities to structured constraints
# def map_to_constraints(extracted_data):
#     constraints = {"max_hours": None, "unavailability": {}, "course_seminary_order": None}
#
#     # Track whether a time period was explicitly mentioned
#     time_range = None
#     days = []
#
#     for entity, label in extracted_data:
#         if label == "DAY":
#             # Map plural days to singular
#             day = map_plural_to_singular(entity)
#             days.append(day)
#
#         elif label == "TIME_RANGE":
#             # Convert time range to start-end time
#             time_range = convert_time_range_to_start_end(entity)
#
#         elif label == "MAX_HOURS":
#             hours = int("".join(filter(str.isdigit, entity)))
#             constraints["max_hours"] = hours
#
#         elif label == "COURSE_SEMINARY_ORDER":
#             constraints["course_seminary_order"] = entity
#
#     # If a time range is found, apply it to each day
#     if time_range:
#         for day in days:
#             constraints["unavailability"][day] = [time_range]
#     else:
#         # If no time range, assign default time range to each day
#         for day in days:
#             constraints["unavailability"][day] = ["08:00-20:00"]
#
#     return constraints
#

# Process professor constraints
# Function to map extracted entities to structured constraints
def map_to_constraints(extracted_data):
    constraints = {"max_hours": None, "unavailability": {}, "course_seminary_order": None}

    # Track whether a time period was explicitly mentioned
    time_range = None
    days = []
    combined_day_time = []  # To store combined day-time constraints

    for i, (entity, label) in enumerate(extracted_data):
        if label == "DAY":
            # Map plural days to singular
            day = map_plural_to_singular(entity)
            if i + 1 < len(extracted_data) and extracted_data[i + 1][1] == "TIME_PERIOD":
                # Combine DAY and TIME_PERIOD
                time_period = extracted_data[i + 1][0]
                combined_day_time.append(f"{day} {time_period}")
            else:
                # If no TIME_PERIOD follows, just add the day
                days.append(day)

        elif label == "TIME_RANGE":
            # Convert time range to start-end time
            time_range = convert_time_range_to_start_end(entity)

        elif label == "MAX_HOURS":
            hours = int("".join(filter(str.isdigit, entity)))
            constraints["max_hours"] = hours

        elif label == "COURSE_SEMINARY_ORDER":
            constraints["course_seminary_order"] = entity

    # If a time range is found, apply it to each day
    if time_range:
        for day in days:
            constraints["unavailability"][day] = [time_range]
    else:
        # If no time range, assign default time range to each day
        for day in days:
            constraints["unavailability"][day] = ["08:00-20:00"]

    # Add the combined day-time constraints
    for day_time in combined_day_time:
        day, time_period = day_time.split(" ", 1)
        time_range = convert_time_range_to_start_end(time_period)
        constraints["unavailability"][day] = [time_range]

    return constraints


structured_professor_data = []
for professor_name, text in professor_constraints:
    entities = extract_constraints(text)
    mapped_constraints = map_to_constraints(entities)
    professor_entry = {
        "full_name": professor_name,
        "subjects": [],  # Add actual subjects here if available
        "constraints": mapped_constraints
    }
    structured_professor_data.append(professor_entry)

# Process student constraints collectively
structured_student_data = {
    "full_name": "students",
    "unavailability": []
}
student_aggregated_constraints = {}

# Aggregate student constraints and count occurrences
student_unavailability_counts = Counter()

for text in student_constraints:
    entities = extract_constraints(text)
    mapped_constraints = map_to_constraints(entities)

    # Aggregate student constraints
    for day, times in mapped_constraints["unavailability"].items():
        if day not in student_aggregated_constraints:
            student_aggregated_constraints[day] = []
        student_aggregated_constraints[day].extend(times)

# Count occurrences of each unavailability across students
for day, times in student_aggregated_constraints.items():
    for time in times:
        student_unavailability_counts[(day, time)] += 1

# Include only unavailabilities that appear more than 5 times
filtered_student_unavailability = {
    day: list(set(times))
    for (day, time), count in student_unavailability_counts.items()
    if count >= 5
    for day, times in student_aggregated_constraints.items() if (day, time) in student_unavailability_counts
}

# Add aggregated student constraints to the structured data if they meet the condition
if filtered_student_unavailability:
    structured_student_data["unavailability"] = [{
        "course": "any",  # Assuming the student constraint applies to any course
        "time": filtered_student_unavailability
    }]

# Combine professor and student data into one list
final_output = structured_professor_data + [structured_student_data]

# Print the final output
print(json.dumps(final_output, indent=4, ensure_ascii=False))