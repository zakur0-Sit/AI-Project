from datetime import datetime
from enum import Enum

class Teacher:
    name: str

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.name}"

    def __eq__(self, other):
        return self.name == other.name

    @staticmethod
    def from_string(string):
        return Teacher(string)

class CourseType(Enum):
    LECTURE = "Curs"
    LABORATORY = "Laborator"
    SEMINAR = "Seminar"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

class Course:
    name: str
    is_optional: bool
    package: int

    def __init__(self, name, is_optional, package):
        self.name = name
        self.is_optional = is_optional
        self.package = package

    def __repr__(self):
        return f"{self.name}{" - optional" if self.is_optional else ""}{f", pachet {self.package}" if self.package else ""}"

    def __eq__(self, other):
        return self.name.strip() == other.name.strip()

    @staticmethod
    def from_string(string):
        name, is_optional, package = string.split(",")
        name = name.strip()
        is_optional = is_optional == "True" or is_optional == "1" or is_optional == "true"
        package = int(package) if package != "" else 0
        return Course(name, is_optional, package)

class Classroom:
    room_id: str

    def __init__(self, room_id):
        self.room_id = room_id

    def __repr__(self):
        return f"{self.room_id}"

    @staticmethod
    def from_string(string):
        return Classroom(string)

class Weekday(Enum):
    MONDAY = "Luni"
    TUESDAY = "Marti"
    WEDNESDAY = "Miercuri"
    THURSDAY = "Joi"
    FRIDAY = "Vineri"
    SATURDAY = "Sambata"
    SUNDAY = "Duminica"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

class TimeInterval:
    interval: tuple[Weekday, datetime, datetime]
    def __init__(self, day_of_week, start_time, end_time):
        self.interval = (Weekday(day_of_week), datetime.strptime(start_time, "%I:%M%p"), datetime.strptime(end_time, "%I:%M%p"))

    def __repr__(self):
        return f"{self.interval[0]}:{self.interval[1].strftime('%I:%M%p')}-{self.interval[2].strftime('%I:%M%p')}"

    @staticmethod
    def from_string(string):
        day_of_week, time_interval = string.split(",")
        day_of_week = Weekday(day_of_week.strip())
        start_time, end_time = time_interval.split("-")
        return TimeInterval(day_of_week, start_time, end_time)

class StudentGroup:
    year: int
    group_id: str

    def __init__(self, year, group_id):
        self.year = year
        self.group_id = group_id

    def __repr__(self):
        return f"{self.year}{self.group_id}"

    @staticmethod
    def from_string(string):
        year, group_id = string.split(",")
        year = int(year)
        return StudentGroup(year, group_id)


class CourseEntry:
    time_interval: TimeInterval
    course: Course
    course_type: CourseType
    group_attendees: list[StudentGroup]
    classroom: Classroom
    teacher: Teacher

    def __init__(self, day_of_week, time_interval, course, course_type, group_attendees, classroom, teacher):
        self.day_of_week = day_of_week
        self.time_interval = time_interval
        self.course = course
        self.course_type = course_type
        self.group_attendees = group_attendees
        self.classroom = classroom
        self.teacher = teacher