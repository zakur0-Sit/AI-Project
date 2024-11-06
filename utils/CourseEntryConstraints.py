from utils.CourseEntry import TimeInterval, Teacher, CourseType, Course, Weekday, StudentGroup, Classroom, CourseEntry

class Constraints:
    teacher_for_course: list[tuple[Teacher, Course, CourseType]]

    teacher_available: list[tuple[Teacher, list[TimeInterval]]]
    teacher_unavailable: list[tuple[Teacher, list[TimeInterval]]]
    teacher_daily_num_of_classes: list[Teacher, list[tuple[Weekday, int]]]

    optional_course_types: list[tuple[Course, list[CourseType]]] # Some courses don't have Lectures

    def __init__(self):
        self.teacher_for_course = []
        self.teacher_available = []
        self.teacher_unavailable = []
        self.teacher_daily_num_of_classes = []
        self.optional_course_types = []

    def add_teacher_for_course_from_string(self, teacher_list, course_list, string):
        teacher, course, course_type = string.split(",")
        teacher = Teacher(teacher)
        course = Course(course,0,0)
        if teacher not in teacher_list or course not in course_list:
            return

        teacher = next((teach for teach in teacher_list if teach == teacher), None)
        course = next((c for c in course_list if c == course), None)
        course_type = CourseType(course_type)

        self.teacher_for_course.append((teacher, course, CourseType(course_type)))

    def add_teacher_available_from_string(self, teacher_list, string):
        teacher, time_interval = string.split(",", 1)
        teacher = Teacher(teacher)
        if teacher not in teacher_list:
            return

        teacher = next((teach for teach in teacher_list if teach == teacher), None)
        time_interval = TimeInterval.from_string(time_interval)
        teacher_tuple = next((teach for teach in self.teacher_available if teach[0] == teacher), None)
        if teacher_tuple:
            teacher_tuple[1].append(time_interval)
        else:
            self.teacher_available.append((teacher, [time_interval]))

    def add_teacher_unavailable_from_string(self, teacher_list, string):
        teacher, time_interval = string.split(",", 1)
        teacher = Teacher(teacher)
        if teacher not in teacher_list:
            return

        teacher = next((teach for teach in teacher_list if teach == teacher), None)
        time_interval = TimeInterval.from_string(time_interval)
        teacher_tuple = next((teach for teach in self.teacher_unavailable if teach[0] == teacher), None)
        if teacher_tuple:
            teacher_tuple[1].append(time_interval)
        else:
            self.teacher_unavailable.append((teacher, [time_interval]))

    def add_teacher_daily_num_of_classes_from_string(self, teacher_list, string):
        teacher, day_of_week, num_of_classes = string.split(",")
        teacher = Teacher(teacher)
        if teacher not in teacher_list:
            return

        teacher = next((teach for teach in teacher_list if teach == teacher), None)
        day_of_week = Weekday(day_of_week)
        num_of_classes = int(num_of_classes)
        teacher_tuple = next((teach for teach in self.teacher_daily_num_of_classes if teach[0] == teacher), None)

        if teacher_tuple:
            teacher_tuple[1].append((day_of_week, num_of_classes))
        else:
            self.teacher_daily_num_of_classes.append((teacher, [(day_of_week, num_of_classes)]))

    def add_optional_course_types_from_string(self, course_list, string):
        course, course_types = string.split(",")
        # print(course, course_types)
        course = Course(course,0,0)
        if course not in course_list:
            return

        course = next((c for c in course_list if c == course), None)
        course_types = [CourseType(course_type) for course_type in course_types.split()]
        print(course)
        print(course_types)
        self.optional_course_types.append((course, course_types))

    def __repr__(self):
        return f"Constrangeri: Profesori - Materii {self.teacher_for_course}\n Profesori - Ore Predare {self.teacher_available}\n Profesori - Ore interzise {self.teacher_unavailable}\n Profesori - Numar ore pe zi {self.teacher_daily_num_of_classes}\n Materii - Tipuri de ore Optionale {self.optional_course_types}"

class TableData:
    faculty_hours: list[TimeInterval]
    courses: list[Course]
    classrooms: list[Classroom]
    student_groups: list[StudentGroup]
    teachers: list[Teacher]

    constraints: Constraints

    courseEntries: list[CourseEntry]  # which will be generated based on the data and constraints above

    # constraint checking methods

    def __init__(self):
        self.faculty_hours = []
        self.courses = []
        self.classrooms = []
        self.student_groups = []
        self.teachers = []
        self.constraints = Constraints()
        self.courseEntries = []

    def __repr__(self):
        return f"TableData: {self.faculty_hours}\n {self.courses}\n {self.classrooms}\n {self.student_groups}\n {self.teachers}\n {self.constraints})"
