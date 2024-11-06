from datetime import datetime
from enum import Enum

class Teacher:
    full_name: str

    def __init__(self, full_name):
        self.full_name = full_name

    def __repr__(self):
        return f"{self.full_name}"

    def __eq__(self, other):
        return self.full_name == other.full_name

    @staticmethod
    def from_string(string):
        return Teacher(string)

class SubjectType(Enum):
    COURSE = "course"
    LABORATORY = "laboratory"
    SEMINAR = "seminary"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

class Course:
    name: str
    is_optional: bool

    def __init__(self, name, is_optional):
        self.name = name
        self.is_optional = is_optional

    def __repr__(self):
        return f"{self.name}"  # - {'optional' if self.is_optional else 'mandatory'}"

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
    def __init__(self, cabinet: str):
        self.cabinet = cabinet

    def __eq__(self, other):
        return self.cabinet == other.cabinet

    def __hash__(self):
        return hash(self.cabinet)

    def __repr__(self):
        return self.cabinet

class TimeInterval:
    def __init__(self, day_of_week: str, start_time: str, end_time: str):
        self.day_of_week = day_of_week.upper()
        self.start_time = datetime.strptime(start_time, "%H:%M")
        self.end_time = datetime.strptime(end_time, "%H:%M")

    def __repr__(self):
        return f"{self.day_of_week}: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"

    def __eq__(self, other):
        if isinstance(other, TimeInterval):
            return (self.day_of_week == other.day_of_week and
                    self.start_time == other.start_time and
                    self.end_time == other.end_time)
        return False

    def __hash__(self):
        return hash((self.day_of_week, self.start_time, self.end_time))

class StudentGroup:
    def __init__(self, group: str):
        self.group = group

    def __repr__(self):
        return f"{self.group}"

    def __hash__(self):
        return hash(self.group)

    def __eq__(self, other):
        return self.group == other.group

class CourseEntry:
    def __init__(self, day_of_week: str, time_interval: TimeInterval, course: Course,
                 course_type: str, group_attendees: list[StudentGroup],
                 classroom: Classroom, teacher: Teacher):
        self.day_of_week = day_of_week
        self.time_interval = time_interval
        self.course = course
        self.course_type = SubjectType[course_type.upper()]
        self.group_attendees = group_attendees
        self.classroom = classroom
        self.teacher = teacher

    def __repr__(self):
        return f"{self.course} ({self.course_type}) in {self.classroom} by {self.teacher} on {self.day_of_week}"