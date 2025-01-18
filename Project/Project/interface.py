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
                r"^(.*?) ~ (.*?) ~ (.*?) ~ (.*?) ~(.*?) ~ (.*?) ~ (.*?)$", line
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

# Funcție pentru afișarea tabelului
def show_schedule(filtered_data, tree):
    for row in tree.get_children():
        tree.delete(row)

    for course in filtered_data:
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

    # Cadru pentru butoane și dropdown
    top_frame = ttk.Frame(frame)
    top_frame.pack(fill="x", pady=10)

    # Butoane pentru schimbarea modului de filtrare
    filter_var = tk.StringVar(value="professor")

    def update_dropdown():
        if filter_var.get() == "professor":
            dropdown_var.set("")
            dropdown_menu["values"] = sorted(set(course[1] for course in courses))
        elif filter_var.get() == "days":
            dropdown_var.set("")
            dropdown_menu["values"] = sorted(DAY_COLORS.keys(), key=lambda x: day_order[x])
        elif filter_var.get() == "subject":
            dropdown_var.set("")
            dropdown_menu["values"] = sorted(set(course[0] for course in courses))

    def filter_data(event=None):
        selected_filter = filter_var.get()
        selected_value = dropdown_var.get()

        if selected_filter == "professor":
            filtered_courses = [course for course in courses if course[1] == selected_value]
        elif selected_filter == "days":
            filtered_courses = [course for course in courses if course[4] == selected_value]
        elif selected_filter == "subject":
            filtered_courses = [course for course in courses if course[0] == selected_value]
        else:
            filtered_courses = courses

        show_schedule(filtered_courses, tree)

    ttk.Button(top_frame, text="Days", command=lambda: filter_var.set("days") or update_dropdown()).pack(side="left", padx=5)
    ttk.Button(top_frame, text="Professor", command=lambda: filter_var.set("professor") or update_dropdown()).pack(side="left", padx=5)
    ttk.Button(top_frame, text="Subject", command=lambda: filter_var.set("subject") or update_dropdown()).pack(side="left", padx=5)

    # Dropdown pentru selectarea valorii filtrului
    dropdown_var = tk.StringVar()
    dropdown_menu = ttk.Combobox(top_frame, textvariable=dropdown_var, state="readonly", width=80)
    dropdown_menu.pack(side="left", padx=10)
    dropdown_menu.bind("<<ComboboxSelected>>", filter_data)

    update_dropdown()

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

    root.mainloop()

create_schedule_app("output_data/output.txt")
