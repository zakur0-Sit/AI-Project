import json
from new.utils.CourseEntry import Classroom, Course, TimeInterval, Teacher, StudentGroup
from new.utils.CourseEntryConstraints import TableData, SoftConstraints
from collections import deque

def ac3(domain_values, courses_info):
    # (Class, Teacher, Stud Group) >> CTS tuple
    # A CTS tuple is actually our node ! per se

    # 2 CTS tuples/nodes are in conflict if they have the same teach or group,
    #       since 1 group can't have 2 entries at the same time
    #       ditto for teacher
    def are_in_conflict(var1, var2):
        _, teacher1, group1 = var1
        _, teacher2, group2 = var2
        return teacher1 == teacher2 or group1 == group2


    def remove_inconsistent_values(xi, xj, domains):
        removed = False
        for x in domains[xi][:]:
            if all(x == y for y in domains[xj]):
                domains[xi].remove(x)
                removed = True
        return removed

    # The actual ac3 algorithm :
    def ac3(arcs, domains):
        queue = deque(arcs)
        while queue:
            (xi, xj) = queue.popleft()
            if remove_inconsistent_values(xi, xj, domains):
                for xk in [arc[0] for arc in arcs if arc[1] == xi]:
                    queue.append((xk, xi))
        return domains

    # Backtracking search for a solution :
    def backtracking_search(variables, domains, arcs):
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

                    local_domains = {v: list(domains[v]) for v in domains}  # Copy of domains
                    local_domains[var] = [value]
                    ac3(arcs, local_domains)

                    result = backtrack(assignment)
                    if result:
                        return result

                    del assignment[var]

            return None

        return backtrack({})

    # We start with our arcs at conflicting CTS nodes,
    #       aka courses taught by the same teacher, or courses for a certain group,
    #       as these cannot happen at the same time! ( aka these should have distinct domain_value )
    arcs = [(v1, v2) for v1 in domain_values for v2 in domain_values if v1 != v2 and are_in_conflict(v1, v2)]

    # Applying the AC3 algo, to remove arc inconsistencies
    domain_values_copy =  {v: list(dom) for v, dom in domain_values.items()}
    reduced_domains = ac3(arcs, domain_values_copy)
    print("Reduced domains after applying AC-3:")
    for var, domain in reduced_domains.items():
        print(f"{var}: {domain}")

    solution = backtracking_search(domain_values, reduced_domains, arcs)
    print("\nSolution found:")
    if solution:
        for var, time_slot in solution.items():
            print(f"{var} - {time_slot}")
    else:
        print("No solution found that satisfies all constraints.")


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
        # table_data.teachers.append(teacher)

        for subject in teacher_data["subjects"]:
            # table_data.courses.append(Course(subject["name"], subject["optional"]))

            table_data.constraints.teacher_for_course.append((teacher, subject["name"]))

            for activity in subject["activities"]:
                # table_data.classrooms.extend([Classroom(cabinet) for cabinet in activity["cabinets"]])

                for group in activity["groups"]:
                    # table_data.student_groups.extend([StudentGroup(group) for group in activity["groups"]])

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

    # -------------------------------------------  Starting AC3 ! -------------------------------------------------------
    # Creating domain_values and courses_info
    #       from the data fetched from our jsons
    domain_values = {}
    courses_info = {}

    # We have a list that contains our 1 json
    # We'll also be working with fixed hours for now (like 8 00, 9 00 ...)
    # To change to using TimeInterval class
    hard_constraints_value = hard_constraints[0]
    start_hour = int(hard_constraints_value["starting_hour"].split(":")[0])
    end_hour = int(hard_constraints_value["ending_hour"].split(":")[0])
    working_days = hard_constraints_value["working_days"]

    time_intervals = []
    for day in working_days:
        for hour in range(start_hour, end_hour): # TimeInterval
            # Working with 1h intervals for start
            # To add class time span, and use that for the below, somehow
            start_time = f"{hour:02d}:00"
            end_time = f"{hour + 1:02d}:00"
            time_intervals.append(TimeInterval(day, start_time, end_time))

    # Setting each (class, teach, group) entry for domain values to default start values
    #       aka  setting values to all the available hours these can take place at (which for now are 1h time spans)
    for course in table_data.courses:
        course_name = course.name
        if course_name not in courses_info:
            courses_info[course_name] = []
        for teacher, course_name in table_data.constraints.teacher_for_course:
            for group in table_data.student_groups:
                variable = (course_name, teacher.full_name, group.group) # domain_value key tuple
                domain_values[variable] = time_intervals.copy() # Setting the starting domain hours aka all the hours

                # Setting the ( Course, Teach, Stud Group ) dependency in courses_info
                courses_info[course.name].append((teacher.full_name, group.group))

    ac3(domain_values, courses_info)