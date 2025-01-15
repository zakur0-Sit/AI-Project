from utils.CourseEntry import TimeInterval, Teacher, SubjectType, Course, StudentGroup, Classroom, CourseEntry

class SoftConstraints:
    def __init__(self):
        self.teacher_for_course_for_groups = []
        self.teacher_available = []
        self.teacher_unavailable = []
        self.teacher_daily_num_of_classes = {}
        self.optional_course_types = []
        self.course_seminary_order = []
        self.students_unavailable = []

    def add_student_unavailable(self, course:Course, time_interval: TimeInterval):
        self.students_unavailable.append((course, time_interval))

    def add_teacher_for_course_for_groups(self, teacher: Teacher, course: Course, course_type: SubjectType, groups: list[StudentGroup]):
        self.teacher_for_course_for_groups.append((teacher, course, course_type, groups))

    # def add_teacher_available(self, teacher: Teacher, time_interval: TimeInterval):
    #     if (teacher, time_interval) not in self.teacher_available:
    #         self.teacher_available.append((teacher, time_interval))

    def add_teacher_unavailable(self, teacher: Teacher, time_interval: TimeInterval):
        self.teacher_unavailable.append((teacher, time_interval))

    def add_teacher_daily_num_of_classes(self, teacher, num_classes):
        self.teacher_daily_num_of_classes[teacher.full_name] = num_classes

    def add_optional_course_types(self, course: Course, course_types: list[SubjectType]):
        self.optional_course_types.append((course, course_types))

    def add_course_seminar_order(self, teacher: Teacher, order: list[SubjectType], time_gap: str):
        self.course_seminary_order.append((teacher, order, time_gap))

    def __repr__(self):
        return (f"SoftConstraints:\n"
                f"Teachers for courses: {self.teacher_for_course_for_groups}\n"
                f"Available teachers: {self.teacher_available}\n"
                f"Unavailable teachers: {self.teacher_unavailable}\n"
                f"Daily number of classes: {self.teacher_daily_num_of_classes}\n"
                f"Optional course types: {self.optional_course_types}\n"
                f"Course seminary order: {self.course_seminary_order}")


class TableData:
    def __init__(self):
        self.courses = []
        self.classrooms = []
        self.student_groups = []
        self.teachers = []
        self.constraints = SoftConstraints()

    def __repr__(self):
        return (f"TableData:\n"
                f"Courses: {self.courses}\n"
                f"Classrooms: {self.classrooms}\n"
                f"Student groups: {self.student_groups}\n"
                f"Teachers: {self.teachers}\n"
                f"SoftConstraints: {self.constraints}")