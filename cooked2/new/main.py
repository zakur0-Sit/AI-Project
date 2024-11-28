import json
from utils.CourseEntry import Classroom, Course, TimeInterval, Teacher, StudentGroup
from utils.CourseEntryConstraints import TableData
from collections import deque

def ac3(domain_values, courses_info):
    def are_in_conflict(var1, var2):
        _, teacher1, group1 = var1
        _, teacher2, group2 = var2
        return teacher1 == teacher2 or group1 == group2

    def remove_inconsistent_values(xi, xj, domains, ignore_constraints):
        removed = False
        for x in domains[xi][:]:
            if not any(x != y for y in domains[xj]) or not soft_constraints_satisfied({xi: x}, ignore_constraints):
                domains[xi].remove(x)
                removed = True
        return removed

    def ac3_internal(arcs, domains, ignore_constraints):
        queue = deque(arcs)
        while queue:
            (xi, xj) = queue.popleft()
            if remove_inconsistent_values(xi, xj, domains, ignore_constraints):
                for xk in [arc[0] for arc in arcs if arc[1] == xi]:
                    queue.append((xk, xi))
        return domains

    def soft_constraints_satisfied(assignment, ignore_constraints=[]):
        teacher_daily_classes = {}

        for var, time_interval in assignment.items():
            if isinstance(time_interval, str):
                day_of_week, times = time_interval.split(": ")
                start_time, end_time = times.split(" - ")
                time_interval = TimeInterval(day_of_week, start_time, end_time)
            teacher_name = var[1]

            if teacher_name not in teacher_daily_classes:
                teacher_daily_classes[teacher_name] = {day: 0 for day in ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]}

            teacher_daily_classes[teacher_name][time_interval.day_of_week] += 1

            if "unavailable_time" not in ignore_constraints:
                for teacher, unavailable_time in table_data.constraints.teacher_unavailable:
                    if isinstance(unavailable_time, str):
                        day_of_week, times = unavailable_time.split(": ")
                        start_time, end_time = times.split(" - ")
                        unavailable_time = TimeInterval(day_of_week, start_time, end_time)
                    if teacher.full_name == teacher_name and time_interval.overlaps(unavailable_time):
                        return False

            if "daily_num_of_classes" not in ignore_constraints:
                for teacher, day_classes in teacher_daily_classes.items():
                    for day, num_classes in day_classes.items():
                        if num_classes > table_data.constraints.teacher_daily_num_of_classes.get((teacher, day), float('inf')):
                            return False

        return True

    def backtracking_search(variables, domains, arcs, ignore_constraints):
        def backtrack(assignment):
            if len(assignment) == len(variables):
                return assignment

            unassigned = [v for v in variables if v not in assignment]
            var = unassigned[0]

            for value in domains[var]:
                consistent = True
                for other_var, other_val in assignment.items():
                    if are_in_conflict(var, other_var) and value == other_val:
                        consistent = False
                        break

                if consistent:
                    assignment[var] = value

                    if soft_constraints_satisfied(assignment, ignore_constraints):
                        local_domains = {v: list(domains[v]) for v in domains}
                        local_domains[var] = [value]
                        ac3_internal(arcs, local_domains, ignore_constraints)

                        result = backtrack(assignment)
                        if result:
                            return result

                    del assignment[var]

            return None

        return backtrack({})

    constraints = ["unavailable_time", "daily_num_of_classes"]
    for i in range(len(constraints) + 1):
        ignore_constraints = constraints[:i]
        arcs = [(v1, v2) for v1 in domain_values for v2 in domain_values if v1 != v2 and are_in_conflict(v1, v2)]
        domain_values_copy = {v: list(dom) for v, dom in domain_values.items()}
        reduced_domains = ac3_internal(arcs, domain_values_copy, ignore_constraints)
        if all(reduced_domains.values()):
            print("Reduced domains after applying AC-3:")
            for var, domain in reduced_domains.items():
                print(f"{var}: {domain}")
            solution = backtracking_search(domain_values, reduced_domains, arcs, ignore_constraints)
            if solution:
                return solution

    return domain_values

if __name__ == "__main__":
    table_data = TableData()

    with open("../input_data/json/teachers.json", encoding='utf-8') as f:
        data = json.load(f)

    with open("../input_data/json/default_values.json", encoding='utf-8') as f:
        default_values = json.load(f)

    with open("../input_data/json/hard_constraints.json", encoding='utf-8') as f:
        hard_constraints = json.load(f)

    for teacher_data in data:
        teacher = Teacher(teacher_data["full_name"])

        for subject in teacher_data["subjects"]:
            table_data.constraints.teacher_for_course.append((teacher, subject["name"]))

            for activity in subject["activities"]:
                for group in activity["groups"]:
                    pass

        for constraint_day, hours in teacher_data["constraints"]["unavailability"].items():
            for hour in hours:
                start_time, end_time = hour.split('-')
                time_interval = TimeInterval(constraint_day, start_time, end_time)
                table_data.constraints.add_teacher_unavailable(teacher, f"{time_interval}")

                daily_num_classes = len(hours)
                table_data.constraints.add_teacher_daily_num_of_classes(teacher, constraint_day.upper(), daily_num_classes)

            if "course_seminar_order" in teacher_data["constraints"]:
                for order_data in teacher_data["constraints"]["course_seminar_order"]:
                    if isinstance(order_data, dict) and "order" in order_data and "time_gap" in orderdata:
                        order = order_data["order"]
                        time_gap = order_data["time_gap"]
                        table_data.constraints.add_course_seminar_order(teacher, order, time_gap)
                    else:
                        print(f"Unexpected data format in course_seminar_order: {order_data}")

    for values in default_values[0]["classes"]:
        table_data.classrooms.append(Classroom(values))

    for values in default_values[0]["groups"]:
        table_data.student_groups.append(StudentGroup(values))

    for values in default_values[0]["professors"]:
        table_data.teachers.append(Teacher(values))

    for course_data in default_values[0]["courses"]:
        name, is_optional = course_data
        course = Course(name, is_optional)
        table_data.courses.append(course)

    table_data.classrooms = list(set(table_data.classrooms))
    table_data.student_groups = list(set(table_data.student_groups))

    print(table_data)

    domain_values = {}
    courses_info = {}

    hard_constraints_value = hard_constraints[0]
    start_hour = int(hard_constraints_value["starting_hour"].split(":")[0])
    end_hour = int(hard_constraints_value["ending_hour"].split(":")[0])
    working_days = hard_constraints_value["working_days"]

    time_intervals = []
    for day in working_days:
        for hour in range(start_hour, end_hour):
            start_time = f"{hour:02d}:00"
            end_time = f"{hour + 1:02d}:00"
            time_intervals.append(TimeInterval(day, start_time, end_time))

    for course in table_data.courses:
        course_name = course.name
        if course_name not in courses_info:
            courses_info[course_name] = []
        for teacher, course_name in table_data.constraints.teacher_for_course:
            for group in table_data.student_groups:
                variable = (course_name, teacher.full_name, group.group)
                domain_values[variable] = time_intervals.copy()

                courses_info[course.name].append((teacher.full_name, group.group))

    solution = ac3(domain_values, courses_info)
    print("\nSolution found:")
    if solution:
        for var, time_slot in solution.items():
            print(f"{var} - {time_slot}")
    else:
        print("No solution found that satisfies all constraints.")