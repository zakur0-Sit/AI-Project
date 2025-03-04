from datetime import datetime
from enum import Enum

WEEK_DAYS = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

class Teacher:
    full_name: str

    def __init__(self, full_name):
        self.full_name = full_name

    def __repr__(self):
        return f"{self.full_name}"

    # def __eq__(self, other):
    #     return self.full_name == other.full_name

    def __eq__(self, other):
        if isinstance(other, Teacher):
            return self.full_name == other.full_name
        return False

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
    is_optional: str

    def __init__(self, name, is_optional):
        self.name = name
        if is_optional == 0:
            is_optional = "obligatoriu"
        elif is_optional == 1:
            is_optional = "optional"
        else:
            is_optional = "facultativ"

        self.is_optional = is_optional

    def __repr__(self):
        return f"{self.name} - {self.is_optional}"  # - {'optional' if self.is_optional else 'mandatory'}"

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

    def time_span(self):
        return self.end_time.hour - self.start_time.hour

    def __repr__(self):
        return f"{self.day_of_week}: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if isinstance(other, TimeInterval):
            return (self.day_of_week == other.day_of_week and
                    self.start_time == other.start_time and
                    self.end_time == other.end_time)
        return False

    def overlaps(self, other):
        return (self.day_of_week == other.day_of_week and
                not (self.end_time <= other.start_time or self.start_time >= other.end_time))

    def __hash__(self):
        return hash((self.day_of_week, self.start_time, self.end_time))

    def __lt__(self, other):
        self_day_of_week_id = WEEK_DAYS.index(self.day_of_week)
        other_day_of_week_id = WEEK_DAYS.index(other.day_of_week)
        return self_day_of_week_id < other_day_of_week_id or (self_day_of_week_id == other_day_of_week_id and self.start_time < other.start_time)

class StudentGroup:
    def __init__(self, year: int, group: str):
        self.year = year
        self.group_label = group

    def __repr__(self):
        return f"{self.year}{self.group_label}"

    def __hash__(self):
        return hash((self.year, self.group_label))

    def __eq__(self, other):
        return self.group_label == other.group_label and self.year == other.year

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