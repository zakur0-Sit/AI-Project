from new.utils.CourseEntry import TimeInterval, Teacher, SubjectType, Course, StudentGroup, Classroom, CourseEntry

class SoftConstraints:
    def __init__(self):
        self.teacher_for_course = []
        self.teacher_available = []
        self.teacher_unavailable = []
        self.teacher_daily_num_of_classes = []
        self.optional_course_types = []

    def add_teacher_for_course(self, teacher: Teacher, course: Course, course_type: SubjectType):
        self.teacher_for_course.append((teacher, course, course_type))

    def add_teacher_available(self, teacher: Teacher, time_interval: TimeInterval):
        if (teacher, time_interval) not in self.teacher_available:
            self.teacher_available.append((teacher, time_interval))

    def add_teacher_unavailable(self, teacher: Teacher, time_interval: TimeInterval):
        self.teacher_unavailable.append((teacher, time_interval))

    def add_teacher_daily_num_of_classes(self, teacher: Teacher, day_of_week, num_of_classes: int):
        self.teacher_daily_num_of_classes.append((teacher, (day_of_week, num_of_classes)))

    def add_optional_course_types(self, course: Course, course_types: list[SubjectType]):
        self.optional_course_types.append((course, course_types))

    def __repr__(self):
        return (f"SoftConstraints:\n"
                f"Teachers for courses: {self.teacher_for_course}\n"
                f"Available teachers: {self.teacher_available}\n"
                f"Unavailable teachers: {self.teacher_unavailable}\n"
                f"Daily number of classes: {self.teacher_daily_num_of_classes}\n"
                f"Optional course types: {self.optional_course_types}")


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
