# # # import re
# # # import spacy
# # # import json
# # # from collections import Counter
# # #
# # # # Load the constraints from the JSON file
# # # with open('constraints.json', 'r') as file:
# # #     constraints_data = json.load(file)
# # #
# # # # Extract professor constraints and student constraints
# # # professor_constraints = constraints_data.get('professor_constraints', [])
# # # student_constraints = constraints_data.get('student_constraints', [])
# # #
# # # # Load the trained model for extracting entities (modify model path as needed)
# # # model_path = "unavailability_model"  # Change to your model's saved path
# # # nlp = spacy.load(model_path)
# # #
# # # # Map plural days to their singular form
# # # plural_to_singular = {
# # #     "Mondays": "Monday",
# # #     "Tuesdays": "Tuesday",
# # #     "Wednesdays": "Wednesday",
# # #     "Thursdays": "Thursday",
# # #     "Fridays": "Friday",
# # #     "Saturdays": "Saturday",
# # #     "Sundays": "Sunday"
# # # }
# # #
# # # # Function to handle singular/plural mapping
# # # def map_plural_to_singular(day):
# # #     return plural_to_singular.get(day, day)
# # #
# # # # Function to extract numeric time difference (e.g., "a day", "two days", "3 days")
# # # def extract_time_difference(text):
# # #     number_map = {
# # #         "a": 1, "one": 1, "two": 2, "three": 3, "four": 4,
# # #         "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
# # #     }
# # #
# # #     time_diff_pattern = r"(seminar|course)\s*(\d+|[a-zA-Z]+)\s*(day|days)\s*(before|after)\s*(seminar|course)"
# # #
# # #     match = re.search(time_diff_pattern, text)
# # #     if match:
# # #         num = match.group(2)
# # #         if num.isdigit():
# # #             num = int(num)
# # #         else:
# # #             num = number_map.get(num.lower(), None)
# # #             if num is None:
# # #                 return None
# # #
# # #         return num * 24
# # #
# # #     if "a day" in text:
# # #         return 24
# # #
# # #     return None
# # #
# # # # Function to extract entities from the text using the model
# # # def extract_constraints(text):
# # #     doc = nlp(text)
# # #     return [(ent.text, ent.label_) for ent in doc.ents]
# # #
# # # # Function to map extracted entities to constraints
# # # def map_to_constraints(extracted_data):
# # #     constraints = {}
# # #
# # #     course_before_seminar = False
# # #     seminar_before_course = False
# # #     time_gap = None
# # #
# # #     time_periods = {
# # #         "morning": "08:00-12:00",
# # #         "afternoon": "12:00-16:00",
# # #         "evening": "16:00-20:00",
# # #         "mornings": "08:00-12:00",
# # #         "afternoons": "12:00-16:00",
# # #         "evenings": "16:00-20:00",
# # #         "after 10 AM": "10:00-20:00",
# # #         "after 12 PM": "12:00-20:00",
# # #         "after 1 PM": "13:00-20:00",
# # #         "after 2 PM": "14:00-20:00",
# # #         "after 3 PM": "15:00-20:00",
# # #         "after 4 PM": "16:00-20:00",
# # #         "after 5 PM": "17:00-20:00",
# # #         "after 6 PM": "18:00-20:00",
# # #         "after 7 PM": "19:00-20:00",
# # #         "before 10 AM": "08:00-10:00",
# # #         "before 12 PM": "08:00-12:00",
# # #         "before 1 PM": "08:00-13:00",
# # #         "before 2 PM": "08:00-14:00",
# # #         "before 3 PM": "08:00-15:00",
# # #         "before 4 PM": "08:00-16:00",
# # #         "before 5 PM": "08:00-17:00",
# # #         "before 6 PM": "08:00-18:00",
# # #         "before 7 PM": "08:00-19:00"
# # #     }
# # #
# # #     for entity, label in extracted_data:
# # #         if label == "DAY":
# # #             day = map_plural_to_singular(entity)
# # #             if "unavailability" not in constraints:
# # #                 constraints["unavailability"] = {}
# # #             if day not in constraints["unavailability"]:
# # #                 constraints["unavailability"][day] = ["08:00-20:00"]
# # #
# # #         elif label == "TIME_PERIOD":
# # #             for day in constraints["unavailability"]:
# # #                 if entity in time_periods:
# # #                     constraints["unavailability"][day] = [time_periods[entity]]
# # #
# # #         elif label == "TIME_RANGE":
# # #             for day in constraints["unavailability"]:
# # #                 constraints["unavailability"][day].append(entity)
# # #
# # #         elif label == "MAX_HOURS":
# # #             hours = int("".join(filter(str.isdigit, entity)))
# # #             constraints["max_hours"] = hours
# # #
# # #         elif label == "COURSE_SEMINARY_ORDER":
# # #             if "before" in entity and "seminar" in entity and "course" in entity:
# # #                 course_before_seminar = True
# # #             elif "after" in entity and "seminar" in entity and "course" in entity:
# # #                 seminar_before_course = True
# # #             elif "before" in entity and "course" in entity and "seminar" in entity:
# # #                 course_before_seminar = True
# # #             elif "after" in entity and "course" in entity and "seminar" in entity:
# # #                 seminar_before_course = True
# # #
# # #     time_gap = extract_time_difference(' '.join([e[0] for e in extracted_data]))
# # #
# # #     if course_before_seminar:
# # #         constraints["course_seminary_order"] = {"first": "course", "time_gap_hours": time_gap}
# # #     elif seminar_before_course:
# # #         constraints["course_seminary_order"] = {"first": "seminar", "time_gap_hours": time_gap}
# # #
# # #     # Remove empty or null constraints
# # #     constraints = {key: value for key, value in constraints.items() if value}
# # #
# # #     return constraints
# # #
# # # # Load the base JSON structure with subjects and activities
# # # with open('utils/sample_teachers.json', 'r', encoding='utf-8') as base_file:
# # #     base_data = json.load(base_file)
# # #
# # # # Update professor constraints into the base structure
# # # for professor in base_data:
# # #     name = professor["full_name"]
# # #     matching_constraint = next((pc for pc in professor_constraints if pc[0] == name), None)
# # #
# # #     if matching_constraint:
# # #         text = matching_constraint[1]
# # #         entities = extract_constraints(text)
# # #         mapped_constraints = map_to_constraints(entities)
# # #         professor["constraints"].update(mapped_constraints)
# # #
# # # # Aggregate student constraints
# # # structured_student_data = next((entry for entry in base_data if entry["full_name"] == "students"), None)
# # # student_aggregated_constraints = {}
# # # student_unavailability_counts = Counter()
# # #
# # # for text in student_constraints:
# # #     entities = extract_constraints(text)
# # #     mapped_constraints = map_to_constraints(entities)
# # #
# # #     for day, times in mapped_constraints["unavailability"].items():
# # #         if day not in student_aggregated_constraints:
# # #             student_aggregated_constraints[day] = []
# # #         student_aggregated_constraints[day].extend(times)
# # #
# # # for day, times in student_aggregated_constraints.items():
# # #     for time in times:
# # #         student_unavailability_counts[(day, time)] += 1
# # #
# # # filtered_student_unavailability = {
# # #     day: list(set(times))
# # #     for (day, time), count in student_unavailability_counts.items()
# # #     if count >= 5
# # #     for day, times in student_aggregated_constraints.items() if (day, time) in student_unavailability_counts
# # # }
# # #
# # # if filtered_student_unavailability:
# # #     structured_student_data["unavailability"] = [{
# # #         "course": "any",
# # #         "time": filtered_student_unavailability
# # #     }]
# # #
# # # # Save the updated JSON to a file
# # # with open('utils/teachers.json', 'w', encoding='utf-8') as f:
# # #     json.dump(base_data, f, indent=2, ensure_ascii=False)
# # #
# # # import re
# # # import spacy
# # # import json
# # # from collections import Counter
# # #
# # # # Load the constraints from the JSON file
# # # with open('constraints.json', 'r') as file:
# # #     constraints_data = json.load(file)
# # #
# # # # Extract professor constraints and student constraints
# # # professor_constraints = constraints_data.get('professor_constraints', [])
# # # student_constraints = constraints_data.get('student_constraints', [])
# # #
# # # # Load the trained model for extracting entities (modify model path as needed)
# # # model_path = "unavailability_model"  # Change to your model's saved path
# # # nlp = spacy.load(model_path)
# # #
# # # # Map plural days to their singular form
# # # plural_to_singular = {
# # #     "Mondays": "Monday",
# # #     "Tuesdays": "Tuesday",
# # #     "Wednesdays": "Wednesday",
# # #     "Thursdays": "Thursday",
# # #     "Fridays": "Friday",
# # #     "Saturdays": "Saturday",
# # #     "Sundays": "Sunday"
# # # }
# # #
# # # # Function to handle singular/plural mapping
# # # def map_plural_to_singular(day):
# # #     return plural_to_singular.get(day, day)
# # #
# # # # Function to extract numeric time difference
# # # def extract_time_difference(text):
# # #     number_map = {
# # #         "a": 1, "one": 1, "two": 2, "three": 3, "four": 4,
# # #         "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
# # #     }
# # #
# # #     time_diff_pattern = r"(seminar|course)\s*(\d+|[a-zA-Z]+)\s*(day|days)\s*(before|after)\s*(seminar|course)"
# # #     match = re.search(time_diff_pattern, text)
# # #     if match:
# # #         num = match.group(2)
# # #         if num.isdigit():
# # #             num = int(num)
# # #         else:
# # #             num = number_map.get(num.lower(), None)
# # #             if num is None:
# # #                 return None
# # #         return num * 24
# # #
# # #     if "a day" in text:
# # #         return 24
# # #
# # #     return None
# # #
# # # # Function to extract entities using the model
# # # def extract_constraints(text):
# # #     doc = nlp(text)
# # #     return [(ent.text, ent.label_) for ent in doc.ents]
# # #
# # # # Function to map extracted entities to constraints
# # # def map_to_constraints(extracted_data):
# # #     constraints = {}
# # #
# # #     course_before_seminar = False
# # #     seminar_before_course = False
# # #     time_gap = None
# # #
# # #     time_periods = {
# # #         "morning": "08:00-12:00",
# # #         "afternoon": "12:00-16:00",
# # #         "evening": "16:00-20:00",
# # #         "after 10 AM": "10:00-20:00",
# # #         "before 10 AM": "08:00-10:00"
# # #     }
# # #
# # #     for entity, label in extracted_data:
# # #         if label == "DAY":
# # #             day = map_plural_to_singular(entity)
# # #             constraints.setdefault("unavailability", {}).setdefault(day, ["08:00-20:00"])
# # #
# # #         elif label == "TIME_PERIOD":
# # #             for day in constraints.get("unavailability", {}):
# # #                 if entity in time_periods:
# # #                     constraints["unavailability"][day] = [time_periods[entity]]
# # #
# # #         elif label == "MAX_HOURS":
# # #             hours = int("".join(filter(str.isdigit, entity)))
# # #             constraints["max_hours"] = hours
# # #
# # #         elif label == "COURSE_SEMINARY_ORDER":
# # #             if "before" in entity:
# # #                 course_before_seminar = True
# # #             elif "after" in entity:
# # #                 seminar_before_course = True
# # #
# # #     time_gap = extract_time_difference(' '.join([e[0] for e in extracted_data]))
# # #
# # #     if course_before_seminar:
# # #         constraints["course_seminary_order"] = {"first": "course", "time_gap_hours": time_gap}
# # #     elif seminar_before_course:
# # #         constraints["course_seminary_order"] = {"first": "seminar", "time_gap_hours": time_gap}
# # #
# # #     constraints = {key: value for key, value in constraints.items() if value}
# # #     return constraints
# # #
# # # # Load the base JSON structure
# # # with open('utils/sample_teachers.json', 'r', encoding='utf-8') as base_file:
# # #     base_data = json.load(base_file)
# # #
# # # # Update professor constraints
# # # for professor in base_data:
# # #     name = professor["full_name"]
# # #     matching_constraint = next((pc for pc in professor_constraints if pc[0] == name), None)
# # #
# # #     if matching_constraint:
# # #         text = matching_constraint[1]
# # #         entities = extract_constraints(text)
# # #         mapped_constraints = map_to_constraints(entities)
# # #         professor["constraints"] = mapped_constraints  # Replace existing constraints
# # #
# # # # Aggregate and replace student constraints
# # # structured_student_data = next((entry for entry in base_data if entry["full_name"] == "students"), None)
# # # student_aggregated_constraints = {}
# # # student_unavailability_counts = Counter()
# # #
# # # for text in student_constraints:
# # #     entities = extract_constraints(text)
# # #     mapped_constraints = map_to_constraints(entities)
# # #
# # #     for day, times in mapped_constraints.get("unavailability", {}).items():
# # #         if day not in student_aggregated_constraints:
# # #             student_aggregated_constraints[day] = []
# # #         student_aggregated_constraints[day].extend(times)
# # #
# # # for day, times in student_aggregated_constraints.items():
# # #     for time in times:
# # #         student_unavailability_counts[(day, time)] += 1
# # #
# # # filtered_student_unavailability = {
# # #     day: list(set(times))
# # #     for (day, time), count in student_unavailability_counts.items()
# # #     if count >= 5
# # #     for day, times in student_aggregated_constraints.items() if (day, time) in student_unavailability_counts
# # # }
# # #
# # # if structured_student_data and filtered_student_unavailability:
# # #     structured_student_data["constraints"] = {
# # #         "unavailability": filtered_student_unavailability
# # #     }
# # #
# # # # Save the updated JSON
# # # with open('utils/teachers.json', 'w', encoding='utf-8') as f:
# # #     json.dump(base_data, f, indent=2, ensure_ascii=False)
# # #
# # #
# # # import re
# # # import spacy
# # # import json
# # # from collections import Counter
# # #
# # # # Load the constraints from the JSON file
# # # with open('constraints.json', 'r') as file:
# # #     constraints_data = json.load(file)
# # #
# # # # Extract professor constraints and student constraints
# # # professor_constraints = constraints_data.get('professor_constraints', [])
# # # student_constraints = constraints_data.get('student_constraints', [])
# # #
# # # # Load the trained model for extracting entities (modify model path as needed)
# # # model_path = "unavailability_model"  # Change to your model's saved path
# # # nlp = spacy.load(model_path)
# # #
# # # # Map plural days to their singular form
# # # plural_to_singular = {
# # #     "Mondays": "Monday",
# # #     "Tuesdays": "Tuesday",
# # #     "Wednesdays": "Wednesday",
# # #     "Thursdays": "Thursday",
# # #     "Fridays": "Friday",
# # #     "Saturdays": "Saturday",
# # #     "Sundays": "Sunday"
# # # }
# # #
# # # # Function to handle singular/plural mapping
# # # def map_plural_to_singular(day):
# # #     return plural_to_singular.get(day, day)
# # #
# # # # Function to extract numeric time difference
# # # def extract_time_difference(text):
# # #     number_map = {
# # #         "a": 1, "one": 1, "two": 2, "three": 3, "four": 4,
# # #         "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
# # #     }
# # #
# # #     time_diff_pattern = r"(seminar|course)\s*(\d+|[a-zA-Z]+)\s*(day|days)\s*(before|after)\s*(seminar|course)"
# # #     match = re.search(time_diff_pattern, text)
# # #     if match:
# # #         num = match.group(2)
# # #         if num.isdigit():
# # #             num = int(num)
# # #         else:
# # #             num = number_map.get(num.lower(), None)
# # #             if num is None:
# # #                 return None
# # #         return num * 24
# # #
# # #     if "a day" in text:
# # #         return 24
# # #
# # #     return None
# # #
# # # # Function to extract entities using the model
# # # def extract_constraints(text):
# # #     doc = nlp(text)
# # #     return [(ent.text, ent.label_) for ent in doc.ents]
# # #
# # # # Function to map extracted entities to constraints
# # # def map_to_constraints(extracted_data):
# # #     constraints = {}
# # #
# # #     course_before_seminar = False
# # #     seminar_before_course = False
# # #     time_gap = None
# # #
# # #     time_periods = {
# # #         "morning": "08:00-12:00",
# # #         "afternoon": "12:00-16:00",
# # #         "evening": "16:00-20:00",
# # #         "after 10 AM": "10:00-20:00",
# # #         "before 10 AM": "08:00-10:00"
# # #     }
# # #
# # #     for entity, label in extracted_data:
# # #         if label == "DAY":
# # #             day = map_plural_to_singular(entity)
# # #             constraints.setdefault("unavailability", {}).setdefault(day, ["08:00-20:00"])
# # #
# # #         elif label == "TIME_PERIOD":
# # #             for day in constraints.get("unavailability", {}):
# # #                 if entity in time_periods:
# # #                     constraints["unavailability"][day] = [time_periods[entity]]
# # #
# # #         elif label == "MAX_HOURS":
# # #             hours = int("".join(filter(str.isdigit, entity)))
# # #             constraints["max_hours"] = hours
# # #
# # #         elif label == "COURSE_SEMINARY_ORDER":
# # #             if "before" in entity:
# # #                 course_before_seminar = True
# # #             elif "after" in entity:
# # #                 seminar_before_course = True
# # #
# # #     time_gap = extract_time_difference(' '.join([e[0] for e in extracted_data]))
# # #
# # #     if course_before_seminar:
# # #         constraints["course_seminary_order"] = {"first": "course", "time_gap_hours": time_gap}
# # #     elif seminar_before_course:
# # #         constraints["course_seminary_order"] = {"first": "seminar", "time_gap_hours": time_gap}
# # #
# # #     constraints = {key: value for key, value in constraints.items() if value}
# # #     return constraints
# # #
# # # # Load the base JSON structure
# # # with open('utils/sample_teachers.json', 'r', encoding='utf-8') as base_file:
# # #     base_data = json.load(base_file)
# # #
# # # # Replace professor constraints
# # # for professor in base_data:
# # #     professor["constraints"] = {}  # Clear existing constraints
# # #     name = professor["full_name"]
# # #     matching_constraint = next((pc for pc in professor_constraints if pc[0] == name), None)
# # #
# # #     if matching_constraint:
# # #         text = matching_constraint[1]
# # #         entities = extract_constraints(text)
# # #         mapped_constraints = map_to_constraints(entities)
# # #         professor["constraints"] = mapped_constraints
# # #
# # # # Aggregate and replace student constraints
# # # structured_student_data = next((entry for entry in base_data if entry["full_name"] == "students"), None)
# # # student_aggregated_constraints = {}
# # # student_unavailability_counts = Counter()
# # #
# # # for text in student_constraints:
# # #     entities = extract_constraints(text)
# # #     mapped_constraints = map_to_constraints(entities)
# # #
# # #     for day, times in mapped_constraints.get("unavailability", {}).items():
# # #         if day not in student_aggregated_constraints:
# # #             student_aggregated_constraints[day] = []
# # #         student_aggregated_constraints[day].extend(times)
# # #
# # # for day, times in student_aggregated_constraints.items():
# # #     for time in times:
# # #         student_unavailability_counts[(day, time)] += 1
# # #
# # # filtered_student_unavailability = {
# # #     day: list(set(times))
# # #     for (day, time), count in student_unavailability_counts.items()
# # #     if count >= 5
# # #     for day, times in student_aggregated_constraints.items() if (day, time) in student_unavailability_counts
# # # }
# # #
# # # if structured_student_data:
# # #     structured_student_data["constraints"] = {
# # #         "unavailability": filtered_student_unavailability
# # #     }
# # #
# # # # Save the updated JSON
# # # with open('utils/teachers.json', 'w', encoding='utf-8') as f:
# # #     json.dump(base_data, f, indent=2, ensure_ascii=False)
# #
# #
# # import re
# # import spacy
# # import json
# # from collections import Counter
# #
# # # Load the constraints from the JSON file
# # with open('constraints.json', 'r') as file:
# #     constraints_data = json.load(file)
# #
# # # Extract professor constraints and student constraints
# # professor_constraints = constraints_data.get('professor_constraints', [])
# # student_constraints = constraints_data.get('student_constraints', [])
# #
# # # Load the trained model for extracting entities (modify model path as needed)
# # model_path = "unavailability_model"  # Change to your model's saved path
# # nlp = spacy.load(model_path)
# #
# # # Map plural days to their singular form
# # plural_to_singular = {
# #     "Mondays": "Monday",
# #     "Tuesdays": "Tuesday",
# #     "Wednesdays": "Wednesday",
# #     "Thursdays": "Thursday",
# #     "Fridays": "Friday",
# #     "Saturdays": "Saturday",
# #     "Sundays": "Sunday"
# # }
# #
# # # Function to handle singular/plural mapping
# # def map_plural_to_singular(day):
# #     return plural_to_singular.get(day, day)
# #
# # # Function to extract numeric time difference (e.g., "a day", "two days", "3 days")
# # def extract_time_difference(text):
# #     number_map = {
# #         "a": 1, "one": 1, "two": 2, "three": 3, "four": 4,
# #         "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
# #     }
# #
# #     time_diff_pattern = r"(seminar|course)\s*(\d+|[a-zA-Z]+)\s*(day|days)\s*(before|after)\s*(seminar|course)"
# #
# #     match = re.search(time_diff_pattern, text)
# #     if match:
# #         num = match.group(2)
# #         if num.isdigit():
# #             num = int(num)
# #         else:
# #             num = number_map.get(num.lower(), None)
# #             if num is None:
# #                 return None
# #
# #         return num * 24
# #
# #     if "a day" in text:
# #         return 24
# #
# #     return None
# #
# # # Function to extract entities from the text using the model
# # def extract_constraints(text):
# #     doc = nlp(text)
# #     return [(ent.text, ent.label_) for ent in doc.ents]
# #
# # # Function to map extracted entities to constraints
# # def map_to_constraints(extracted_data):
# #     constraints = {}
# #
# #     course_before_seminar = False
# #     seminar_before_course = False
# #     time_gap = None
# #
# #     time_periods = {
# #         "morning": "08:00-12:00",
# #         "afternoon": "12:00-16:00",
# #         "evening": "16:00-20:00",
# #         "mornings": "08:00-12:00",
# #         "afternoons": "12:00-16:00",
# #         "evenings": "16:00-20:00",
# #         "after 10 AM": "10:00-20:00",
# #         "after 12 PM": "12:00-20:00",
# #         "after 1 PM": "13:00-20:00",
# #         "after 2 PM": "14:00-20:00",
# #         "after 3 PM": "15:00-20:00",
# #         "after 4 PM": "16:00-20:00",
# #         "after 5 PM": "17:00-20:00",
# #         "after 6 PM": "18:00-20:00",
# #         "after 7 PM": "19:00-20:00",
# #         "before 10 AM": "08:00-10:00",
# #         "before 12 PM": "08:00-12:00",
# #         "before 1 PM": "08:00-13:00",
# #         "before 2 PM": "08:00-14:00",
# #         "before 3 PM": "08:00-15:00",
# #         "before 4 PM": "08:00-16:00",
# #         "before 5 PM": "08:00-17:00",
# #         "before 6 PM": "08:00-18:00",
# #         "before 7 PM": "08:00-19:00"
# #     }
# #
# #     for entity, label in extracted_data:
# #         if label == "DAY":
# #             day = map_plural_to_singular(entity)
# #             if "unavailability" not in constraints:
# #                 constraints["unavailability"] = {}
# #             if day not in constraints["unavailability"]:
# #                 constraints["unavailability"][day] = ["08:00-20:00"]
# #
# #         elif label == "TIME_PERIOD":
# #             for day in constraints.get("unavailability", {}):
# #                 if entity in time_periods:
# #                     constraints["unavailability"][day] = [time_periods[entity]]
# #
# #         elif label == "TIME_RANGE":
# #             for day in constraints.get("unavailability", {}):
# #                 constraints["unavailability"][day].append(entity)
# #
# #         elif label == "MAX_HOURS":
# #             hours = int("".join(filter(str.isdigit, entity)))
# #             constraints["max_hours"] = hours
# #
# #         elif label == "COURSE_SEMINARY_ORDER":
# #             if "before" in entity and "seminar" in entity and "course" in entity:
# #                 course_before_seminar = True
# #             elif "after" in entity and "seminar" in entity and "course" in entity:
# #                 seminar_before_course = True
# #             elif "before" in entity and "course" in entity and "seminar" in entity:
# #                 course_before_seminar = True
# #             elif "after" in entity and "course" in entity and "seminar" in entity:
# #                 seminar_before_course = True
# #
# #     time_gap = extract_time_difference(' '.join([e[0] for e in extracted_data]))
# #
# #     if course_before_seminar:
# #         constraints["course_seminary_order"] = {"first": "course", "time_gap_hours": time_gap}
# #     elif seminar_before_course:
# #         constraints["course_seminary_order"] = {"first": "seminar", "time_gap_hours": time_gap}
# #
# #     # Add default max_hours if not set
# #     if "max_hours" not in constraints:
# #         constraints["max_hours"] = 10
# #
# #     # Remove empty or null constraints
# #     constraints = {key: value for key, value in constraints.items() if value}
# #
# #     return constraints
# #
# # # Load the base JSON structure with subjects and activities
# # with open('utils/test_teachers.json', 'r', encoding='utf-8') as base_file:
# #     base_data = json.load(base_file)
# #
# # # Update professor constraints into the base structure
# # for professor in base_data:
# #     name = professor["full_name"]
# #     matching_constraint = next((pc for pc in professor_constraints if pc[0] == name), None)
# #
# #     if matching_constraint:
# #         text = matching_constraint[1]
# #         entities = extract_constraints(text)
# #         mapped_constraints = map_to_constraints(entities)
# #         professor["constraints"] = mapped_constraints  # Fully replace constraints
# #
# # # Aggregate student constraints
# # structured_student_data = next((entry for entry in base_data if entry["full_name"] == "students"), None)
# # student_aggregated_constraints = {}
# # student_unavailability_counts = Counter()
# #
# # for text in student_constraints:
# #     entities = extract_constraints(text)
# #     mapped_constraints = map_to_constraints(entities)
# #
# #     for day, times in mapped_constraints.get("unavailability", {}).items():
# #         if day not in student_aggregated_constraints:
# #             student_aggregated_constraints[day] = []
# #         student_aggregated_constraints[day].extend(times)
# #
# # for day, times in student_aggregated_constraints.items():
# #     for time in times:
# #         student_unavailability_counts[(day, time)] += 1
# #
# # filtered_student_unavailability = {
# #     day: list(set(times))
# #     for (day, time), count in student_unavailability_counts.items()
# #     if count >= 5
# #     for day, times in student_aggregated_constraints.items() if (day, time) in student_unavailability_counts
# # }
# #
# # if filtered_student_unavailability:
# #     structured_student_data["unavailability"] = [{
# #         "course": "any",
# #         "time": filtered_student_unavailability
# #     }]
# #
# # # Print to see constraints
# #
# #
# # # Save the updated JSON to a new file
# # with open('utils/teachers.json', 'w', encoding='utf-8') as f:
# #     json.dump(base_data, f, indent=2, ensure_ascii=False)
#

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
    number_map = {
        "a": 1, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }

    time_diff_pattern = r"(seminar|course)\s*(\d+|[a-zA-Z]+)\s*(day|days)\s*(before|after)\s*(seminar|course)"

    match = re.search(time_diff_pattern, text)
    if match:
        num = match.group(2)
        if num.isdigit():
            num = int(num)
        else:
            num = number_map.get(num.lower(), None)
            if num is None:
                return None

        return num * 24

    if "a day" in text:
        return 24

    return None

# Function to extract entities from the text using the model
def extract_constraints(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

# Function to map extracted entities to constraints
def map_to_constraints(extracted_data):
    constraints = {}

    course_before_seminar = False
    seminar_before_course = False
    time_gap = None

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

    for entity, label in extracted_data:
        if label == "DAY":
            day = map_plural_to_singular(entity)
            if "unavailability" not in constraints:
                constraints["unavailability"] = {}
            if day not in constraints["unavailability"]:
                constraints["unavailability"][day] = ["08:00-20:00"]

        elif label == "TIME_PERIOD":
            for day in constraints["unavailability"]:
                if entity in time_periods:
                    constraints["unavailability"][day] = [time_periods[entity]]

        elif label == "TIME_RANGE":
            for day in constraints["unavailability"]:
                constraints["unavailability"][day].append(entity)

        elif label == "MAX_HOURS":
            hours = int("".join(filter(str.isdigit, entity)))
            constraints["max_hours"] = hours

        elif label == "COURSE_SEMINARY_ORDER":
            if "before" in entity and "seminar" in entity and "course" in entity:
                course_before_seminar = True
            elif "after" in entity and "seminar" in entity and "course" in entity:
                seminar_before_course = True
            elif "before" in entity and "course" in entity and "seminar" in entity:
                course_before_seminar = True
            elif "after" in entity and "course" in entity and "seminar" in entity:
                seminar_before_course = True

    time_gap = extract_time_difference(' '.join([e[0] for e in extracted_data]))

    if course_before_seminar:
        constraints["course_seminary_order"] = {"first": "course", "time_gap_hours": time_gap}
    elif seminar_before_course:
        constraints["course_seminary_order"] = {"first": "seminar", "time_gap_hours": time_gap}

    # Remove empty or null constraints
    constraints = {key: value for key, value in constraints.items() if value}

    return constraints

# Load the base JSON structure with subjects and activities
with open('utils/test_teachers.json', 'r', encoding='utf-8') as base_file:
    base_data = json.load(base_file)

# Update professor constraints into the base structure
for professor in base_data:
    name = professor["full_name"]
    matching_constraint = next((pc for pc in professor_constraints if pc[0] == name), None)

    if matching_constraint:
        text = matching_constraint[1]
        entities = extract_constraints(text)
        mapped_constraints = map_to_constraints(entities)
        professor["constraints"].update(mapped_constraints)

# Aggregate student constraints
structured_student_data = next((entry for entry in base_data if entry["full_name"] == "students"), None)
student_aggregated_constraints = {}
student_unavailability_counts = Counter()

for text in student_constraints:
    entities = extract_constraints(text)
    mapped_constraints = map_to_constraints(entities)

    for day, times in mapped_constraints["unavailability"].items():
        if day not in student_aggregated_constraints:
            student_aggregated_constraints[day] = []
        student_aggregated_constraints[day].extend(times)

for day, times in student_aggregated_constraints.items():
    for time in times:
        student_unavailability_counts[(day, time)] += 1

filtered_student_unavailability = {
    day: list(set(times))
    for (day, time), count in student_unavailability_counts.items()
    if count >= 5
    for day, times in student_aggregated_constraints.items() if (day, time) in student_unavailability_counts
}

if filtered_student_unavailability:
    structured_student_data["unavailability"] = [{
        "course": "any",
        "time": filtered_student_unavailability
    }]

# Save the updated JSON to a file
with open('utils/teachers.json', 'w', encoding='utf-8') as f:
    json.dump(base_data, f, indent=2, ensure_ascii=False)