import tkinter as tk
from tkinter import ttk
import interface

def create_constraints_app(professors):
    def add_constraint():
        professor = professor_var.get()
        professor_constraint = constraint_entry.get().strip()

        if professor and professor_constraint:
            constraints_list.append([professor, professor_constraint])
            display_constraint(professor, professor_constraint)
            constraint_entry.delete(0, tk.END)

    def add_student_constraint():
        student_constraint = student_constraint_entry.get().strip()

        if student_constraint:
            student_constraints_list.append(student_constraint)
            display_student_constraint(student_constraint)
            student_constraint_entry.delete(0, tk.END)

    def display_constraint(professor, constraint):
        frame = tk.Frame(constraints_frame, bg="#F0F8FF")
        frame.pack(fill="x", pady=2)

        label = tk.Label(frame, text=f"{professor}: {constraint}", anchor="w", bg="#F0F8FF")
        label.pack(side="left", fill="x", expand=True, padx=5)

        delete_button = tk.Button(frame, text=" X ", bg="#FF9999", command=lambda: delete_constraint(frame, professor, constraint))
        delete_button.pack(side="right", padx=5)

    def display_student_constraint(student_constraint):
        frame = tk.Frame(student_constraints_frame, bg="#FFFACD")
        frame.pack(fill="x", pady=2)

        label = tk.Label(frame, text=f"Student: {student_constraint}", anchor="w", bg="#FFFACD")
        label.pack(side="left", fill="x", expand=True, padx=5)

        delete_button = tk.Button(frame, text=" X ", bg="#FF9999", command=lambda: delete_student_constraint(frame, student_constraint))
        delete_button.pack(side="right", padx=5)

    def delete_constraint(frame, professor, constraint):
        constraints_list.remove([professor, constraint])
        frame.destroy()

    def delete_student_constraint(frame, student_constraint):
        student_constraints_list.remove(student_constraint)
        frame.destroy()

    def close_window():
        root.destroy()
        return constraints_list,  student_constraints_list

    root = tk.Tk()
    root.title("Gestionare Constrângeri")
    root.geometry("1600x800")

    top_frame = ttk.Frame(root)
    top_frame.pack(pady=10)

    prof_frame = ttk.Frame(top_frame)
    prof_frame.pack(padx=20, side="left")

    constraint_frame = ttk.Frame(top_frame)
    constraint_frame.pack(padx=20, side="left")

    # Dropdown pentru selectarea profesorului
    ttk.Label(prof_frame, text="Select Professor:").pack(pady=5)
    professor_var = tk.StringVar()
    professor_menu = ttk.Combobox(prof_frame, textvariable=professor_var, values=professors, state="readonly", width=30)
    professor_menu.pack(pady=5)

    # Textbox pentru adăugarea constrângerii
    ttk.Label(constraint_frame, text="Professor's constraint:").pack(pady=5)
    constraint_entry = ttk.Entry(constraint_frame, width=50)
    constraint_entry.pack(pady=5)

    # Buton pentru a adăuga constrângerea
    add_button = tk.Button(top_frame, text="Add Professor Constraint", command=add_constraint, bg="#98FB98", bd=0, width=40, height=2)
    add_button.pack(pady=20, padx=20, side="left")

    student_constraints_frame = tk.Frame(top_frame)
    student_constraints_frame.pack(padx=20, side="left")

    ttk.Label(student_constraints_frame, text="Student's constraint:").pack(pady=5)
    student_constraint_entry = ttk.Entry(student_constraints_frame, width=50)
    student_constraint_entry.pack(pady=5)

    add_student_button = tk.Button(top_frame, text="Add Student Constraint", command=add_student_constraint, bg="#98FB98", bd=0, width=40, height=2)
    add_student_button.pack(pady=20, padx=20, side="left")

    # Zonă pentru lista de constrângeri
    result_frame = tk.Frame(root)
    result_frame.pack(fill="both", expand=True, pady=5, padx=5)

    result_professors_frame = tk.Frame(result_frame)
    result_professors_frame.pack(fill="both", expand=True, pady=5, padx=5, side="left")

    result_students_frame = tk.Frame(result_frame)
    result_students_frame.pack(fill="both", expand=True, pady=5, padx=5, side="left")

    tk.Label(result_professors_frame, text="Professors Constraints:").pack(pady=5)
    constraints_frame = tk.Frame(result_professors_frame, bg="#F0F8FF")
    constraints_frame.pack(fill="both", pady=5, padx=5)

    tk.Label(result_students_frame, text="Students Constraints:").pack(pady=5)
    student_constraints_frame = tk.Frame(result_students_frame, bg="#FFFACD")
    student_constraints_frame.pack(fill="both",  pady=5, padx=5)

    # Zonă separată pentru butonul de salvare
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(fill="x", pady=10)

    save_button = tk.Button(bottom_frame, text="Save and Close", command=close_window, bg="#ADD8E6", bd=0, width=40, height=2)
    save_button.pack(anchor="center", pady=10)

    # Lista de constrângeri
    constraints_list = []
    student_constraints_list = []

    root.mainloop()

# Exemplu de utilizare
course = interface.read_and_sort_schedule("output_data/output.txt")
professors = []
for curs in course:
    if curs[1] not in professors:
        professors.append(curs[1])

create_constraints_app(professors)
