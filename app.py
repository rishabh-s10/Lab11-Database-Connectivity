
import tkinter as tk
from tkinter import ttk, messagebox
import db

root = tk.Tk()
root.title("Film/Theatre Production Management")
root.geometry("1200x700")
root.configure(bg="#f2f4f7")

title = tk.Label(
    root,
    text="PERSON MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold"),
    bg="#f2f4f7"
)
title.pack(pady=15)

subtitle = tk.Label(
    root,
    text="Film/Theatre Production Database",
    font=("Arial", 11),
    bg="#f2f4f7"
)
subtitle.pack()

form = tk.LabelFrame(
    root,
    text="Person Details",
    font=("Arial", 12, "bold"),
    padx=15,
    pady=15,
    bg="#f2f4f7"
)
form.pack(fill="x", padx=20, pady=15)

labels = [
    "Person ID",
    "Full Name",
    "Department",
    "Availability",
    "Phone",
    "Email",
    "Emergency Contact"
]

entries = []

for i, label in enumerate(labels):
    row = i // 2
    col = (i % 2) * 2

    tk.Label(
        form,
        text=label,
        bg="#f2f4f7",
        font=("Arial", 10)
    ).grid(row=row, column=col, padx=10, pady=8, sticky="w")

    if label == "Department":
        entry = ttk.Combobox(
            form,
            values=["Production", "Technical", "Costume", "Administration"],
            state="readonly",
            width=27
        )

    elif label == "Availability":
        entry = ttk.Combobox(
            form,
            values=["Available", "Busy"],
            state="readonly",
            width=27
        )

    else:
        entry = tk.Entry(form, width=30)

    entry.grid(row=row, column=col + 1, padx=10, pady=8)
    entries.append(entry)


def get_values():
    values = [entry.get().strip() for entry in entries]

    if any(value == "" for value in values):
        messagebox.showerror("Error", "Please fill all fields")
        return None

    try:
        values[0] = int(values[0])
    except ValueError:
        messagebox.showerror("Error", "Person ID must be an integer")
        return None

    return values


def clear_fields():
    for entry in entries:
        entry.delete(0, tk.END)


def refresh_table():
    for item in table.get_children():
        table.delete(item)

    try:
        people = db.get_people()

        for person in people:
            table.insert("", tk.END, values=person)

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


def add_record():
    values = get_values()

    if values is None:
        return

    try:
        rows = db.add_person(*values)

        if rows == 1:
            messagebox.showinfo("Success", "Person added successfully!")
            clear_fields()
            refresh_table()
        else:
            messagebox.showwarning("Notice", "No record was inserted.")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def select_record(event):
    selected = table.focus()

    if not selected:
        return

    values = table.item(selected, "values")

    clear_fields()

    for i, value in enumerate(values):
        entries[i].insert(0, value)


def update_record():
    selected = table.focus()

    if not selected:
        messagebox.showerror("Error", "Select a person from the table first")
        return

    values = get_values()

    if values is None:
        return

    try:
        rows = db.update_person(*values)

        if rows == 1:
            messagebox.showinfo("Success", "Person updated successfully!")
            clear_fields()
            refresh_table()
        else:
            messagebox.showwarning("Notice", "Person not found.")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def delete_record():
    selected = table.focus()

    if not selected:
        messagebox.showerror("Error", "Select a person first")
        return

    values = table.item(selected, "values")
    person_id = int(values[0])

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this person?"
    )

    if confirm:
        try:
            rows = db.delete_person(person_id)

            if rows == 1:
                messagebox.showinfo("Success", "Person deleted successfully!")
                clear_fields()
                refresh_table()
            else:
                messagebox.showwarning("Notice", "Person not found.")

        except Exception as e:
            messagebox.showerror("Error", str(e))


button_frame = tk.Frame(root, bg="#f2f4f7")
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Add Person",
    width=16,
    command=add_record,
    bg="#2e8b57",
    fg="white"
).grid(row=0, column=0, padx=8)

tk.Button(
    button_frame,
    text="Update Person",
    width=16,
    command=update_record,
    bg="#2874a6",
    fg="white"
).grid(row=0, column=1, padx=8)

tk.Button(
    button_frame,
    text="Delete Person",
    width=16,
    command=delete_record,
    bg="#c0392b",
    fg="white"
).grid(row=0, column=2, padx=8)

tk.Button(
    button_frame,
    text="Refresh",
    width=16,
    command=refresh_table
).grid(row=0, column=3, padx=8)


table_frame = tk.LabelFrame(
    root,
    text="Personnel Records",
    font=("Arial", 12, "bold"),
    bg="#f2f4f7",
    padx=10,
    pady=10
)
table_frame.pack(fill="both", expand=True, padx=20, pady=15)

columns = (
    "person_id",
    "full_name",
    "department",
    "availability",
    "phone",
    "email",
    "emergency_contact"
)

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for column in columns:
    table.heading(column, text=column.replace("_", " ").title())
    table.column(column, width=145, anchor="center")

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=table.yview
)

table.configure(yscrollcommand=scrollbar.set)

table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

table.bind("<<TreeviewSelect>>", select_record)

refresh_table()

root.mainloop()