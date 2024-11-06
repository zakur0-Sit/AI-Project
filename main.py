from utils.CourseEntry import Classroom, Course, TimeInterval, Teacher, StudentGroup
from utils.CourseEntryConstraints import TableData

# Example usage:
if __name__ == "__main__":

    table_data = TableData()
    file = open("input_data/faculty_timeinterval.csv", encoding='utf-8').readlines()
    for line in file:
        table_data.faculty_hours.append(TimeInterval.from_string(line.strip()))

    file = open("input_data/courses.csv", encoding='utf-8').readlines()
    for line in file:
        table_data.courses.append(Course.from_string(line.strip()))

    file = open("input_data/classrooms.csv", encoding='utf-8').readlines()
    for line in file:
        table_data.classrooms.append(Classroom.from_string(line.strip()))

    file = open("input_data/student_groups.csv", encoding='utf-8').readlines()
    for line in file:
        table_data.student_groups.append(StudentGroup.from_string(line.strip()))

    file = open("input_data/teachers.csv", encoding='utf-8').readlines()
    for line in file:
        table_data.teachers.append(Teacher.from_string(line.strip()))

    ##
    file = open("input_data/teacher_course.csv", encoding='utf-8').readlines()
    for line in file:
        table_data.constraints.add_teacher_for_course_from_string(table_data.teachers, table_data.courses, line.strip())

    file = open("input_data/teacher_timeinterval.csv", encoding='utf-8').readlines()
    for line in file:
        table_data.constraints.add_teacher_available_from_string(table_data.teachers, line.strip())

    file = open("input_data/teacher_unavailabletimeintervals.csv", encoding='utf-8').readlines()
    for line in file:
        table_data.constraints.add_teacher_unavailable_from_string(table_data.teachers, line.strip())

    file = open("input_data/teacher_daily_classes.csv", encoding='utf-8').readlines()
    for line in file:
        table_data.constraints.add_teacher_daily_num_of_classes_from_string(table_data.teachers, line.strip())

    file = open("input_data/course_optionaltypes.csv", encoding='utf-8').readlines()
    for line in file:
        table_data.constraints.add_optional_course_types_from_string(table_data.courses, line.strip())

    print(table_data)