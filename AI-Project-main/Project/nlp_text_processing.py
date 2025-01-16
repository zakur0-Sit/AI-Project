# import re
# import spacy
# import json
# from collections import Counter
#
# # Load the constraints from the JSON file
# with open('constraints.json', 'r') as file:
#     constraints_data = json.load(file)
#
# # Extract professor constraints and student constraints
# professor_constraints = constraints_data.get('professor_constraints', [])
# student_constraints = constraints_data.get('student_constraints', [])
#
# # Load the trained model for extracting entities (modify model path as needed)
# model_path = "unavailability_model"  # Change to your model's saved path
# nlp = spacy.load(model_path)
#
# # Map plural days to their singular form
# plural_to_singular = {
#     "Mondays": "Monday",
#     "Tuesdays": "Tuesday",
#     "Wednesdays": "Wednesday",
#     "Thursdays": "Thursday",
#     "Fridays": "Friday",
#     "Saturdays": "Saturday",
#     "Sundays": "Sunday"
# }
#
# # Function to handle singular/plural mapping
# def map_plural_to_singular(day):
#     return plural_to_singular.get(day, day)
#
# # Function to extract numeric time difference (e.g., "a day", "two days", "3 days")
# def extract_time_difference(text):
#     # Mapping common word representations of numbers
#     number_map = {
#         "a": 1, "one": 1, "two": 2, "three": 3, "four": 4,
#         "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
#     }
#
#     # Time difference pattern for matching 'a day' or other time gap expressions
#     time_diff_pattern = r"(seminar|course)\s*(\d+|[a-zA-Z]+)\s*(day|days)\s*(before|after)\s*(seminar|course)"
#
#     # Check if there is a match in the text for the time difference pattern
#     match = re.search(time_diff_pattern, text)
#     if match:
#         num = match.group(2)
#         if num.isdigit():
#             num = int(num)
#         else:
#             # Handle the "a day" case and convert it to 1 day (24 hours)
#             num = number_map.get(num.lower(), None)
#             if num is None:
#                 return None
#
#         # Return the time gap in hours (24 hours for a day)
#         return num * 24
#
#     # return 24 hours for a day
#     if "a day" in text:
#         return 24  # Return 24 hours if "a day" is found
#
#     return None
#
# # Function to extract entities from the text using the model
# def extract_constraints(text):
#     doc = nlp(text)
#     return [(ent.text, ent.label_) for ent in doc.ents]
#
# # Function to map extracted entities to constraints
# def map_to_constraints(extracted_data):
#     constraints = {"max_hours": None, "unavailability": {}, "course_seminary_order": None}
#
#     # Flag to detect order (before or after)
#     course_before_seminar = False
#     seminar_before_course = False
#     time_gap = None
#
#     # Define time mappings for "after X PM" or "after X AM"
#     time_periods = {
#         "morning": "08:00-12:00",
#         "afternoon": "12:00-16:00",
#         "evening": "16:00-20:00",
#         "mornings": "08:00-12:00",
#         "afternoons": "12:00-16:00",
#         "evenings": "16:00-20:00",
#         "after 10 AM": "10:00-20:00",
#         "after 12 PM": "12:00-20:00",
#         "after 1 PM": "13:00-20:00",
#         "after 2 PM": "14:00-20:00",
#         "after 3 PM": "15:00-20:00",
#         "after 4 PM": "16:00-20:00",
#         "after 5 PM": "17:00-20:00",
#         "after 6 PM": "18:00-20:00",
#         "after 7 PM": "19:00-20:00",
#         "before 10 AM": "08:00-10:00",
#         "before 12 PM": "08:00-12:00",
#         "before 1 PM": "08:00-13:00",
#         "before 2 PM": "08:00-14:00",
#         "before 3 PM": "08:00-15:00",
#         "before 4 PM": "08:00-16:00",
#         "before 5 PM": "08:00-17:00",
#         "before 6 PM": "08:00-18:00",
#         "before 7 PM": "08:00-19:00"
#     }
#
#     # Handle extracting and structuring constraints
#     for entity, label in extracted_data:
#         if label == "DAY":
#             # Map plural days to singular
#             day = map_plural_to_singular(entity)
#             if day not in constraints["unavailability"]:
#                 constraints["unavailability"][day] = ["08:00-20:00"]  # Default time range
#
#         elif label == "TIME_PERIOD":
#             # Directly match time period expressions and map to fixed time ranges
#             for day in constraints["unavailability"]:
#                 if entity in time_periods:
#                     constraints["unavailability"][day] = [time_periods[entity]]  # Override with specific time period
#
#         elif label == "TIME_RANGE":
#             for day in constraints["unavailability"]:
#                 constraints["unavailability"][day].append(entity)
#
#         elif label == "MAX_HOURS":
#             hours = int("".join(filter(str.isdigit, entity)))
#             constraints["max_hours"] = hours
#
#         elif label == "COURSE_SEMINARY_ORDER":
#             # Detect the pattern of course-seminary order
#             if "before" in entity and "seminar" in entity and "course" in entity:
#                 course_before_seminar = True
#             elif "after" in entity and "seminar" in entity and "course" in entity:
#                 seminar_before_course = True
#             elif "before" in entity and "course" in entity and "seminar" in entity:
#                 course_before_seminar = True
#             elif "after" in entity and "course" in entity and "seminar" in entity:
#                 seminar_before_course = True
#
#     # Extract time gap for course-seminary order
#     time_gap = extract_time_difference(' '.join([e[0] for e in extracted_data]))
#
#     # Set course-seminary order based on detected patterns
#     if course_before_seminar:
#         constraints["course_seminary_order"] = {"first": "course", "time_gap_hours": time_gap}
#     elif seminar_before_course:
#         constraints["course_seminary_order"] = {"first": "seminar", "time_gap_hours": time_gap}
#
#     return constraints
#
# structured_professor_data = []
# for professor_name, text in professor_constraints:
#     entities = extract_constraints(text)
#     mapped_constraints = map_to_constraints(entities)
#     professor_entry = {
#         "full_name": professor_name,
#         "subjects": [],  # Add actual subjects here if available
#         "constraints": mapped_constraints
#     }
#     structured_professor_data.append(professor_entry)
#
# # Process student constraints collectively
# structured_student_data = {
#     "full_name": "students",
#     "unavailability": []
# }
# student_aggregated_constraints = {}
#
# # Aggregate student constraints and count occurrences
# student_unavailability_counts = Counter()
#
# for text in student_constraints:
#     entities = extract_constraints(text)
#     mapped_constraints = map_to_constraints(entities)
#
#     # Aggregate student constraints
#     for day, times in mapped_constraints["unavailability"].items():
#         if day not in student_aggregated_constraints:
#             student_aggregated_constraints[day] = []
#         student_aggregated_constraints[day].extend(times)
#
# # Count occurrences of each unavailability across students
# for day, times in student_aggregated_constraints.items():
#     for time in times:
#         student_unavailability_counts[(day, time)] += 1
#
# # Include only unavailabilities that appear more than 5 times
# filtered_student_unavailability = {
#     day: list(set(times))
#     for (day, time), count in student_unavailability_counts.items()
#     if count >= 5
#     for day, times in student_aggregated_constraints.items() if (day, time) in student_unavailability_counts
# }
#
# # Add aggregated student constraints to the structured data if they meet the condition
# if filtered_student_unavailability:
#     structured_student_data["unavailability"] = [{
#         "course": "any",  # Assuming the student constraint applies to any course
#         "time": filtered_student_unavailability
#     }]
#
# # Combine professor and student data into one list
# final_output = structured_professor_data + [structured_student_data]
#
# # Print the final output
# print(json.dumps(final_output, indent=4, ensure_ascii=False))
#
# # Write the final output to train.json file
# with open('utils/teachers.json', 'w', encoding='utf-8') as f:
#     json.dump(final_output, f, indent=2, ensure_ascii=False)

import re
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

# Function to extract numeric time difference (e.g., "a day", "two days", "3 days")
def extract_time_difference(text):
    # Mapping common word representations of numbers
    number_map = {
        "a": 1, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }

    # Time difference pattern for matching 'a day' or other time gap expressions
    time_diff_pattern = r"(seminar|course)\s*(\d+|[a-zA-Z]+)\s*(day|days)\s*(before|after)\s*(seminar|course)"

    # Check if there is a match in the text for the time difference pattern
    match = re.search(time_diff_pattern, text)
    if match:
        num = match.group(2)
        if num.isdigit():
            num = int(num)
        else:
            # Handle the "a day" case and convert it to 1 day (24 hours)
            num = number_map.get(num.lower(), None)
            if num is None:
                return None

        # Return the time gap in hours (24 hours for a day)
        return num * 24

    # return 24 hours for a day
    if "a day" in text:
        return 24  # Return 24 hours if "a day" is found

    return None

# Function to extract entities from the text using the model
def extract_constraints(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

# Function to map extracted entities to constraints
def map_to_constraints(extracted_data):
    constraints = {"max_hours": 20, "unavailability": {}, "course_seminary_order": None}

    # Flag to detect order (before or after)
    course_before_seminar = False
    seminar_before_course = False
    time_gap = None

    # Define time mappings for "after X PM" or "after X AM"
    time_periods = {
        "morning": "08:00-12:00",
        "afternoon": "12:00-16:00",
        "evening": "16:00-20:00",
        "mornings": "08:00-12:00",
        "afternoons": "12:00-16:00",
        "evenings": "16:00-20:00",
        "after 10 AM": "10:00-20:00",
        "after 12 PM": "12:00-20:00",
        "after 1 PM": "13:00-20:00",
        "after 2 PM": "14:00-20:00",
        "after 3 PM": "15:00-20:00",
        "after 4 PM": "16:00-20:00",
        "after 5 PM": "17:00-20:00",
        "after 6 PM": "18:00-20:00",
        "after 7 PM": "19:00-20:00",
        "before 10 AM": "08:00-10:00",
        "before 12 PM": "08:00-12:00",
        "before 1 PM": "08:00-13:00",
        "before 2 PM": "08:00-14:00",
        "before 3 PM": "08:00-15:00",
        "before 4 PM": "08:00-16:00",
        "before 5 PM": "08:00-17:00",
        "before 6 PM": "08:00-18:00",
        "before 7 PM": "08:00-19:00"
    }

    # Handle extracting and structuring constraints
    for entity, label in extracted_data:
        if label == "DAY":
            # Map plural days to singular
            day = map_plural_to_singular(entity)
            if day not in constraints["unavailability"]:
                constraints["unavailability"][day] = ["08:00-20:00"]  # Default time range

        elif label == "TIME_PERIOD":
            # Directly match time period expressions and map to fixed time ranges
            for day in constraints["unavailability"]:
                if entity in time_periods:
                    constraints["unavailability"][day] = [time_periods[entity]]  # Override with specific time period

        elif label == "TIME_RANGE":
            for day in constraints["unavailability"]:
                constraints["unavailability"][day].append(entity)

        elif label == "MAX_HOURS":
            hours = int("".join(filter(str.isdigit, entity)))
            constraints["max_hours"] = hours

        elif label == "COURSE_SEMINARY_ORDER":
            # Detect the pattern of course-seminary order
            if "before" in entity and "seminar" in entity and "course" in entity:
                course_before_seminar = True
            elif "after" in entity and "seminar" in entity and "course" in entity:
                seminar_before_course = True
            elif "before" in entity and "course" in entity and "seminar" in entity:
                course_before_seminar = True
            elif "after" in entity and "course" in entity and "seminar" in entity:
                seminar_before_course = True

    # Extract time gap for course-seminary order
    time_gap = extract_time_difference(' '.join([e[0] for e in extracted_data]))

    # Set course-seminary order based on detected patterns
    if course_before_seminar:
        constraints["course_seminary_order"] = {"first": "course", "time_gap_hours": time_gap}
    elif seminar_before_course:
        constraints["course_seminary_order"] = {"first": "seminar", "time_gap_hours": time_gap}

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

# Write the final output to train.json file
with open('utils/teachers.json', 'w', encoding='utf-8') as f:
    json.dump(final_output, f, indent=2, ensure_ascii=False)