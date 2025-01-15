import tkinter as tk
from tkinter import ttk
import re

# Dictionar pentru culori în funcție de zi
DAY_COLORS = {
    "MONDAY": "#FFCCCC",
    "TUESDAY": "#FFE5CC",
    "WEDNESDAY": "#FFFFCC",
    "THURSDAY": "#E5FFCC",
    "FRIDAY": "#CCE5FF",
    "SATURDAY": "#E5CCFF",
    "SUNDAY": "#FFCCE5",
}

# Dictionar pentru ordinea zilelor săptămânii
day_order = {
    "MONDAY": 0,
    "TUESDAY": 1,
    "WEDNESDAY": 2,
    "THURSDAY": 3,
    "FRIDAY": 4,
    "SATURDAY": 5,
    "SUNDAY": 6,
}

# Funcție pentru citirea fișierului și extragerea datelor
def read_and_sort_schedule(file_path):
    courses = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            match = re.match(
                r"^(.*?): (.*?) - (.*?) - (.*?): \((.*?): (.*?), '(.*?)'\)$", line
            )
            if match:
                title = match.group(1).strip()
                instructor = match.group(2).strip()
                group = match.group(3).strip()
                activity = match.group(4).strip()
                day = match.group(5).strip()
                time = match.group(6).strip()
                room = match.group(7).strip()

                courses.append((title, instructor, group, activity, day, time, room))

    sorted_courses = sorted(
        courses,
        key=lambda x: (x[1], day_order.get(x[4], 7), x[5])
    )
    return sorted_courses

# Funcție pentru afișarea tabelului în funcție de profesor
def show_schedule_by_instructor(selected_instructor, courses, tree):
    for row in tree.get_children():
        tree.delete(row)

    filtered_courses = [course for course in courses if course[1] == selected_instructor]

    for course in filtered_courses:
        day = course[4]
        color = DAY_COLORS.get(day, "white")

        tree.insert("", "end", values=course, tags=(day,))

    for day, color in DAY_COLORS.items():
        tree.tag_configure(day, background=color)

# Funcție principală pentru interfață
def create_schedule_app(file_path):
    courses = read_and_sort_schedule(file_path)

    root = tk.Tk()
    root.title("Orar Profesori")

    # Creăm un cadru pentru meniu și tabel
    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)

    # Dropdown pentru selectarea profesorului
    instructor_label = ttk.Label(frame, text="Selectează Profesorul:")
    instructor_label.pack(padx=10, pady=5)

    instructors = sorted(set(course[1] for course in courses))
    instructor_var = tk.StringVar()
    instructor_menu = ttk.Combobox(frame, textvariable=instructor_var, values=instructors, state="readonly", width=100)
    instructor_menu.pack(padx=10, pady=5)

    # Tabelul (Treeview)
    columns = ("Disciplina", "Profesor", "Grup", "Activitate", "Ziua", "Interval", "Sala")
    tree = ttk.Treeview(frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.pack(fill="both", expand=True, padx=10, pady=5)

    # Scrollbar pentru tabel
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Legăm selecția din meniu de actualizarea tabelului
    def on_instructor_select(event):
        selected_instructor = instructor_var.get()
        show_schedule_by_instructor(selected_instructor, courses, tree)

    instructor_menu.bind("<<ComboboxSelected>>", on_instructor_select)

    root.mainloop()

create_schedule_app("output_data/output.txt")
