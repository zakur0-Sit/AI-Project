import json
from new.utils.CourseEntry import Classroom, Course, TimeInterval, Teacher, StudentGroup
from new.utils.CourseEntryConstraints import TableData, Constraints

if __name__ == "__main__":
    table_data = TableData()

    with open("teachers.json", encoding='utf-8') as f:
        data = json.load(f)

    for teacher_data in data:
        teacher = Teacher(teacher_data["full_name"])
        table_data.teachers.append(teacher)

        for subject in teacher_data["subjects"]:
            table_data.courses.append(Course(subject["name"], subject["optional"]))

            table_data.constraints.teacher_for_course.append((teacher, subject["name"]))

            for activity in subject["activities"]:
                table_data.classrooms.extend([Classroom(cabinet) for cabinet in activity["cabinets"]])

                for group in activity["groups"]:
                    table_data.student_groups.extend([StudentGroup(group) for group in activity["groups"]])

                    for day, hours in activity["days"].items():
                        for hour in hours:
                            start_time, end_time = hour.split('-')
                            table_data.constraints.add_teacher_available(teacher, TimeInterval(day, start_time, end_time))

        for constraint_day, hours in teacher_data["constraints"]["unavailability"].items():
            for hour in hours:
                start_time, end_time = hour.split('-')
                time_interval = TimeInterval(constraint_day, start_time, end_time)
                table_data.constraints.add_teacher_unavailable(teacher, f"{time_interval}")

                daily_num_classes = len(hours)
                table_data.constraints.add_teacher_daily_num_of_classes(teacher, constraint_day.upper(), daily_num_classes)

    table_data.classrooms = list(set(table_data.classrooms))
    table_data.student_groups = list(set(table_data.student_groups))

    print(table_data)
