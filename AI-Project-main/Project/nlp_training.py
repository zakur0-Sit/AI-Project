# import spacy
# import re
# from spacy.training.example import Example
# import random
#
# # Load the pre-trained model
# nlp = spacy.load('en_core_web_sm')
#
# # Check if 'ner' pipeline exists, if not, add it
# if "ner" not in nlp.pipe_names:
#     ner = nlp.add_pipe("ner", last=True)
# else:
#     ner = nlp.get_pipe("ner")
#
# # Add custom entity labels to the NER pipeline
# for label in ["DAY", "TIME_PERIOD", "TIME_RANGE", "MAX_HOURS", "COURSE_SEMINARY_ORDER"]:
#     ner.add_label(label)
#
# # Define patterns for time-based expressions
# patterns = [
#     {"label": "TIME_RANGE", "pattern": [{"lower": "after"}, {"like_num": True}, {"lower": "pm"}]},
#     {"label": "TIME_RANGE", "pattern": [{"lower": "after"}, {"like_num": True}, {"lower": "am"}]},
#     {"label": "TIME_PERIOD", "pattern": [{"lower": "morning"}]},
#     {"label": "TIME_PERIOD", "pattern": [{"lower": "mornings"}]},
#     {"label": "TIME_PERIOD", "pattern": [{"lower": "afternoon"}]},
#     {"label": "TIME_PERIOD", "pattern": [{"lower": "afternoons"}]},
#     {"label": "TIME_PERIOD", "pattern": [{"lower": "evening"}]},
#     {"label": "TIME_PERIOD", "pattern": [{"lower": "evenings"}]},
#     {"label": "TIME_RANGE", "pattern": [{"lower": "before"}, {"like_num": True}, {"lower": "pm"}]},
#     {"label": "TIME_RANGE", "pattern": [{"lower": "before"}, {"like_num": True}, {"lower": "am"}]},
#     {"label": "DAY", "pattern": [{"lower": "monday"}]},
#     {"label": "DAY", "pattern": [{"lower": "tuesday"}]},
#     {"label": "DAY", "pattern": [{"lower": "wednesday"}]},
#     {"label": "DAY", "pattern": [{"lower": "thursday"}]},
#     {"label": "DAY", "pattern": [{"lower": "friday"}]},
#     {"label": "DAY", "pattern": [{"lower": "saturday"}]},
#     {"label": "DAY", "pattern": [{"lower": "sunday"}]},
# ]
#
# # Add EntityRuler to the pipeline and add the patterns
# ruler = nlp.add_pipe("entity_ruler", before="ner")
# ruler.add_patterns(patterns)
#
# # Define your custom training data
# train_data = [
#     ("I'm free on Tuesday mornings and Thursday afternoons.", {"entities": [(12, 19, "DAY"), (20, 29, "TIME_PERIOD"), (33, 41, "DAY"), (42, 52, "TIME_PERIOD")]}),
#     ("I'm free on Monday mornings and Tuesday afternoons.", {"entities": [(12, 19, "DAY"), (19, 28, "TIME_PERIOD"), (32, 40, "DAY"), (40, 50, "TIME_PERIOD")]}),
#     ("I only work in the afternoons on Wednesdays.", {"entities": [(19, 29, "TIME_PERIOD"), (33, 43, "DAY")]}),
#     ("I can't attend class after 2 PM on Tuesdays and Thursdays.", {"entities": [(21, 31, "TIME_PERIOD"), (35, 43, "DAY"), (48, 57, "DAY")]}),
#     ("I'm unavailable on weekends.", {"entities": [(19, 27, "DAY")]}),
#     ("Please schedule my classes only after 3 PM.", {"entities": [(32, 42, "TIME_RANGE")]}),
#     ("I cannot attend class after 6 PM.", {"entities": [(22, 32, "TIME_RANGE")]}),
#     ("No classes before 4 PM on Thursdays.", {"entities": [(11, 22, "TIME_RANGE"), (26, 35, "DAY")]}),
#     ("No classes before 10 AM on Thursdays.", {"entities": [(11, 23, "TIME_RANGE"), (27, 36, "DAY")]}),
#     ("No classes before 2 PM on Mondays.", {"entities": [(11, 22, "TIME_RANGE"), (26, 33, "DAY")]}),
#     ("I want to have the seminar a day before the course.", {"entities": [(19, 50, "COURSE_SEMINARY_ORDER")]}),
#     ("I want to have the course a day after the seminar.", {"entities": [(19, 50, "COURSE_SEMINARY_ORDER")]}),
#     ("I want to have the seminar a day after the course.", {"entities": [(19, 50, "COURSE_SEMINARY_ORDER")]}),
#     ("I want to have the course a day before the seminar.", {"entities": [(19, 50, "COURSE_SEMINARY_ORDER")]}),
#     ("I would want to have the seminar a day before the course.", {"entities": [(25, 56, "COURSE_SEMINARY_ORDER")]}),
#     ("I would like to have the course a day before the seminar.", {"entities": [(25, 57, "COURSE_SEMINARY_ORDER")]}),
#     ("I would like to have the course two days before the seminar.", {"entities": [(25, 60, "COURSE_SEMINARY_ORDER")]}),
#     ("I would want to have the seminar two days after the course.", {"entities": [(25, 59, "COURSE_SEMINARY_ORDER")]}),
#     ("I want to have less than 3 hours of classes per day.", {"entities": [(25, 43, "MAX_HOURS")]}),
#     ("I need to have less than 4 hours of classes on Mondays.", {"entities": [(25, 43, "MAX_HOURS")]}),
#     ("I need to have a maximum of 2 hours of classes on Tuesdays.", {"entities": [(28, 46, "MAX_HOURS")]}),
#     ("I can handle a maximum of 6 hours of classes per day.", {"entities": [(26, 44, "MAX_HOURS")]}),
#     ("I can handle a maximum of 4 hours of classes per day.", {"entities": [(26, 44, "MAX_HOURS")]}),
# ]
#
# # Preview the training data entities discovered
# for text, annotations in train_data:
#     print(f"Text: {text}")
#     print("Entities:")
#     for start, end, label in annotations["entities"]:
#         print(f"  - {text[start:end]} ({label})")
#     print("-" * 50)
#
#
# # Start training the model
# # optimizer = nlp.begin_training()
# optimizer = nlp.resume_training()
#
# # Train the model
# for epoch in range(50):  # Train for more epochs
#     random.shuffle(train_data)
#     losses = {}
#     # Convert the training data into Example objects
#     train_examples = []
#     for text, annotations in train_data:
#         doc = nlp.make_doc(text)
#         example = Example.from_dict(doc, annotations)
#         train_examples.append(example)
#
#     # Update the model with each batch
#     nlp.update(train_examples, drop=0.5, losses=losses)
#     print(f"Epoch {epoch} - Losses: {losses}")
#
# # Test the model with a new sentence
# test_text = "I can attend class before 2 PM on Saturdays and Thursdays."
# doc = nlp(test_text)
#
# # Extract the entities
# extracted_entities = [(ent.text, ent.label_) for ent in doc.ents]
# print("Extracted Entities:", extracted_entities)
#
# # Test with another sentence
# # test_text2 = "I want classes on Monday mornings and Friday afternoons."
# test_text2 = "I would want to have the course one day before the seminar."
# doc2 = nlp(test_text2)
# extracted_entities2 = [(ent.text, ent.label_) for ent in doc2.ents]
# print("Extracted Entities:", extracted_entities2)
#
# test_text3 = "I want classes on Monday mornings and Friday afternoons."
# #test_text3 = "I want to have less than 5 hours of classes per day."
# doc3 = nlp(test_text3)
# extracted_entities3 = [(ent.text, ent.label_) for ent in doc3.ents]
# print("Extracted Entities:", extracted_entities3)
#
#
# nlp.to_disk("unavailability_model")

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