import io
import json
import os
import sys

from utils.CourseEntry import Classroom, Course, TimeInterval, Teacher, StudentGroup, WEEK_DAYS
from utils.CourseEntryConstraints import TableData
from collections import deque

def build_ignore_soft_constraints(table_data):
    ignore_constraints = {"unavailable_time" : [], "daily_num_of_classes" : [], "course_seminary_order" : []}

    for teacher, _ in table_data.constraints.teacher_unavailable:
        ignore_constraints["unavailable_time"].append(teacher.full_name)

    for teacher_name, _ in table_data.constraints.teacher_daily_num_of_classes.keys():
        ignore_constraints["daily_num_of_classes"].append(teacher_name)

    for teacher, order, time_gap_hours in table_data.constraints.course_seminary_order:
        ignore_constraints["course_seminary_order"].append(teacher.full_name)

    return ignore_constraints


def ac3(domain_values):
    def are_in_conflict(var1, var2):
        _, teacher1, group1, _ = var1
        _, teacher2, group2, _ = var2
        # check if no numbers are in group1
        if any(char.isdigit() for char in group1) and any(char.isdigit() for char in group2):
            return teacher1 == teacher2 or group1 == group2

        semi_year1, semi_year2 = [], []
        for semi_year in ["A", "B", "E"]:
            if semi_year in group1:
                semi_year1.append(semi_year)
            if semi_year in group2:
                semi_year2.append(semi_year)

        return teacher1 == teacher2 or any(semi_year in semi_year2 for semi_year in semi_year1)

    def remove_inconsistent_values(xi, xj, domains, ignore_constraints):
        removed = False
        for x in domains[xi][:]:
            if not arc_constraints_satisfied(xi, x, xj, domains, ignore_constraints):
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


    def arc_constraints_satisfied(xi, i_value, xj, domains, ignore_constraints={}):
        _, i_teacher, _, i_type = xi
        _, j_teacher, _, j_type = xj

        found_any_j_value = False
        for j_value in domains[xj]:
            if not isinstance(domains[xj], list):
                j_value = domains[xj]

            ok_value = True
            if i_value == j_value:
                ok_value = False
                continue

            # course_seminary_order arc constraint
            teacher_with_course_seminary_order = [teach.full_name for teach, _, _ in table_data.constraints.course_seminary_order]
            a = "course_seminary_order" not in ignore_constraints.keys()
            b = 0
            if not a:
              b = i_teacher not in ignore_constraints["course_seminary_order"]
            c = i_teacher in teacher_with_course_seminary_order
            d = i_teacher == j_teacher
            e = i_type != j_type
            if ("course_seminary_order" not in ignore_constraints.keys() or
                    i_teacher not in ignore_constraints["course_seminary_order"]) and i_teacher in teacher_with_course_seminary_order and \
                    i_teacher == j_teacher and i_type != j_type:
                which_is_first, time_gap_hours = [(order, time_gap_hours) \
                                                  for teach, order, time_gap_hours in table_data.constraints.course_seminary_order if teach.full_name == i_teacher][0]


                i_time_interval, j_time_interval = 0, 0
                # try:
                i_time_interval, j_time_interval = i_value[0], j_value[0]
                # except:
                #     print("i_value: " + str(i_value))
                #     print("j_value: " + str(j_value))
                #     print("xi:" + str(xi))
                #     print("xj:" + str(xj))


                i_day_of_week_id, j_day_of_week_id = list(WEEK_DAYS).index(i_time_interval.day_of_week), list(WEEK_DAYS).index(j_time_interval.day_of_week)

                i_minus_j_time_gap = abs((i_day_of_week_id * 24 + i_value[0].start_time.hour) - (j_day_of_week_id * 24 + j_value[0].start_time.hour))
                if i_time_interval < j_time_interval and i_type == which_is_first and i_minus_j_time_gap >= time_gap_hours:
                        # ok_value = True
                        pass # idk how to write these ifs so I wrote them like so
                elif j_time_interval < i_time_interval and j_type == which_is_first and i_minus_j_time_gap >= time_gap_hours:
                        # ok_value = True
                        pass # idk how to write these ifs so I wrote them like so
                else:
                    ok_value = False
                    continue

            if ok_value: # found one j value for which the constraint is satisfied
                found_any_j_value = True
                break

        if not found_any_j_value:
            return False
        else:
            return True

    def backtracking_soft_constraints_satisfied(assignment, ignore_constraints={}):
        # spacing :P

        for xi in assignment.keys():
            for xj in assignment.keys():
                pass
                if xi != xj and not arc_constraints_satisfied(xi, assignment[xi], xj, assignment, ignore_constraints):
                    return False

                # other soft constraints that can only be imposed at backtracking, cuz they're not arc like
                available_teachers_with_daily_maximum_hours = []
                for teacher, _ in table_data.constraints.teacher_daily_num_of_classes.keys():
                    if "daily_num_of_classes" not in ignore_constraints or \
                            teacher not in ignore_constraints.get("daily_num_of_classes", []):
                        available_teachers_with_daily_maximum_hours.append(teacher)

                teacher_hours_per_day = {}
                for var in assignment.keys():
                    time_interval, _ = assignment[var]
                    teacher_name = var[1]
                    if teacher_name not in available_teachers_with_daily_maximum_hours:
                        continue

                    if teacher_name not in teacher_hours_per_day:
                        teacher_hours_per_day[teacher_name] = {day: 0 for day in
                                                               ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY",
                                                                "SATURDAY"]}
                    teacher_hours_per_day[teacher_name][time_interval.day_of_week] += time_interval.time_span() # num of hours

                for teacher, day_classes in teacher_hours_per_day.items():
                    for day, num_classes in day_classes.items():
                        if num_classes > table_data.constraints.teacher_daily_num_of_classes.get((teacher, day), float('inf')):
                            return False

        return True

    # def soft_constraints_satisfied(assignment, ignore_constraints={}):
    #     teacher_daily_classes = {}
    #     courses_data = {}
    #
    #     for var in assignment.keys():
    #         time_interval, _ = assignment[var]
    #         if isinstance(time_interval, str):
    #             day_of_week, times = time_interval.split(": ")
    #             start_time, end_time = times.split(" - ")
    #             time_interval = TimeInterval(day_of_week, start_time, end_time)
    #         teacher_name = var[1]
    #         course_name = var[0]
    #         course_type = var[3]
    #
    #         if teacher_name not in teacher_daily_classes:
    #             teacher_daily_classes[teacher_name] = {day: 0 for day in
    #                                                    ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY",
    #                                                     "SATURDAY"]}
    #
    #         teacher_daily_classes[teacher_name][time_interval.day_of_week] += 1
    #
    #         if teacher_name not in ignore_constraints.get("unavailable_time", []):
    #             for teacher, unavailable_time in table_data.constraints.teacher_unavailable:
    #                 if isinstance(unavailable_time, str):
    #                     day_of_week, times = unavailable_time.split(": ")
    #                     start_time, end_time = times.split(" - ")
    #                     unavailable_time = TimeInterval(day_of_week, start_time, end_time)
    #                 if teacher.full_name == teacher_name and time_interval.overlaps(unavailable_time):
    #                     return False
    #
    #         if teacher_name not in ignore_constraints.get("daily_num_of_classes", []):
    #             for teacher, day_classes in teacher_daily_classes.items():
    #                 for day, num_classes in day_classes.items():
    #                     if num_classes > table_data.constraints.teacher_daily_num_of_classes.get((teacher, day),
    #                                                                                              float('inf')):
    #                         return False
    #
    #         if teacher_name not in ignore_constraints.get("course_seminary_order", []):
    #             if course_name not in courses_data:
    #                 courses_data[course_name] = []
    #
    #             courses_data[course_name].append((time_interval, course_type))
    #
    #     print("\n\n table data and course data")
    #     print(table_data.constraints.course_seminary_order)
    #     print(courses_data)
    #     print("\n\n")
    #     for teacher, order, time_gap_hours in table_data.constraints.course_seminary_order:
    #         print("\n\n entry in course_seminary_order")
    #         print(teacher.full_name + " " + order + " " + str(time_gap_hours))
    #         print("ignore constains: " + str(ignore_constraints))
    #         if teacher.full_name in ignore_constraints.get("course_seminary_order", []):
    #             continue
    #
    #         print("aici")
    #
    #         for course_name, courses_list in courses_data.items():
    #             for i in range(len(courses_list) - 1):
    #                 current_time_interval, current_course_type = courses_list[i]
    #                 next_time_interval, next_course_type = courses_list[i + 1]
    #                 print("\n\n course data entries")
    #                 print(course_name)
    #                 print(current_time_interval)
    #                 print(current_course_type)
    #                 print(next_time_interval)
    #                 print(next_course_type)
    #                 print(order)
    #                 print(time_gap_hours)
    #                 print("\n\n")
    #
    #                 current_day_of_week_id = list(WEEK_DAYS).index(current_time_interval.day_of_week)
    #                 next_day_of_week_id = list(WEEK_DAYS).index(next_time_interval.day_of_week)
    #
    #                 current_time = current_day_of_week_id * 24 + current_time_interval.start_time.hour
    #                 next_time = next_day_of_week_id * 24 + next_time_interval.start_time.hour
    #
    #                 if current_course_type == "seminary" and next_course_type == "course" and order == "seminary":
    #                     if next_time - current_time < time_gap_hours:
    #                         return False
    #                 elif current_course_type == "course" and next_course_type == "seminary" and order == "course":
    #                     if next_time - current_time < time_gap_hours:
    #                         return False
    #                 else:
    #                     return False
    #
    #     return True

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

                    if backtracking_soft_constraints_satisfied(assignment, ignore_constraints):
                        local_domains = {v: list(domains[v]) for v in domains}
                        local_domains[var] = [value]
                        ac3_internal(arcs, local_domains, ignore_constraints)

                        result = backtrack(assignment)
                        if result:
                            return result

                    del assignment[var]

            return None

        return backtrack({})

    soft_constraints = build_ignore_soft_constraints(table_data)
    soft_constrains_amount = sum([len(constrained_items) for constrained_items in soft_constraints.values()])
    for i in range(soft_constrains_amount + 1):
        # we first try to make a solution without ignoring constraints, then just one, and so on
        # we'll decrease from the number of constraints to ignore till 0
        ignore_constraints = {}
        num_of_constraints_to_ignore = i
        for constrain_type in soft_constraints.keys():
            if num_of_constraints_to_ignore == 0:
                break

            for constrained_items in soft_constraints[constrain_type]:
                if num_of_constraints_to_ignore == 0:
                    break

                if constrain_type not in ignore_constraints:
                    ignore_constraints[constrain_type] = []
                ignore_constraints[constrain_type].append(constrained_items)
                num_of_constraints_to_ignore -= 1

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

    # Open a file to write the output
    output_file = open('./output_data/logs.txt', 'w')
    # Redirect stdout to the file
    sys.stdout = io.TextIOWrapper(output_file.buffer, encoding='utf-8')


    table_data = TableData()

    with open("./utils/teachers.json", encoding='utf-8') as f:
        data = json.load(f)

    with open("./utils/default_values.json", encoding='utf-8') as f:
        default_values = json.load(f)

    with open("../input_data/json/hard_constraints.json", encoding='utf-8') as f:
        hard_constraints = json.load(f)

    for teacher_data in data:
        teacher = Teacher(teacher_data["full_name"])

        for subject in teacher_data["subjects"]:
            for activity in subject["activities"]:
                table_data.constraints.add_teacher_for_course_for_groups(teacher, subject["name"], activity["type"], activity["groups"])


        for constraint_day, hours in teacher_data["constraints"]["unavailability"].items():
            for hour in hours:
                start_time, end_time = hour.split('-')
                time_interval = TimeInterval(constraint_day, start_time, end_time)
                table_data.constraints.add_teacher_unavailable(teacher, f"{time_interval}")

                daily_num_classes = len(hours)
                table_data.constraints.add_teacher_daily_num_of_classes(teacher, constraint_day.upper(), daily_num_classes)

            if "course_seminary_order" in teacher_data["constraints"]:
                order_data = teacher_data["constraints"]["course_seminary_order"]
                if isinstance(order_data, dict) and "first" in order_data and "time_gap_hours" in order_data:
                    which_is_first = order_data["first"]
                    time_gap_hours = order_data["time_gap_hours"]
                    table_data.constraints.add_course_seminar_order(teacher, which_is_first, time_gap_hours)
                else:
                    print(f"Unexpected data format in course_seminar_order: {order_data}")

    for values in default_values[0]["classes"]:
        table_data.classrooms.append(Classroom(values))

    student_years = default_values[0]["years"]
    student_groups = default_values[0]["groups"]
    for year in student_years:
        for group in student_groups:
            table_data.student_groups.append(StudentGroup(year, group))

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
        for hour in range(start_hour, end_hour, 2):
            if start_hour % 2 == 1: # presupun ca avem doar ore de 2 ore, la ore pare ; TODO
                continue

            start_time = f"{hour:02d}:00"
            end_time = f"{hour + 2:02d}:00"
            time_intervals.append(TimeInterval(day, start_time, end_time))


    print("table data" + str(table_data))

    for course in table_data.courses:
        course_name = course.name
        # if course_name not in courses_info:
            # courses_info[course_name] = []

        for teacher, course_name, course_type, group_list in table_data.constraints.teacher_for_course_for_groups:
            for group in group_list:
                for classroom in table_data.classrooms:
                    variable = (course_name, teacher.full_name, group, course_type)
                    domain_values[variable] = [(time_i, classroom) for time_i in time_intervals.copy()]

                    # courses_info[course.name].append((teacher.full_name, group, classroom.cabinet))

    solution = ac3(domain_values)
    sol_str = ""
    print("\nSolution found:")
    if solution:
        print(solution)

        for var, time_slot in solution.items():
            sol_str += f"{var[0]}: {var[1]} - {var[2]} - {var[3]}: {time_slot}\n"
    else:
        print("No solution found that satisfies all constraints.")

    os.makedirs("./output_data", exist_ok=True)
    with open("./output_data/output.txt", "w", encoding='utf-8') as f:
        f.write(sol_str)