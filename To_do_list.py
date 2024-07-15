# TO-DO LIST


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sql

def add_task():
    task_entry = task_field.get()

    if len(task_entry) == 0:
        messagebox.showinfo('Error', 'Field is Empty.')
    else:
        tasks.append(task_entry)
        the_cursor.execute('insert into tasks values (?)', (task_entry,))
        update_task_list()
        task_field.delete(0, 'end')

def update_task_list():
    clear_task_list()
    for task in tasks:
        task_listbox.insert('end', task)

def delete_selected_task():
    try:
        selected_task = task_listbox.get(task_listbox.curselection())

        if selected_task in tasks:
            tasks.remove(selected_task)
            update_task_list()
            the_cursor.execute('delete from tasks where title = ?', (selected_task,))
    except:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

def delete_all_tasks():
    confirmation = messagebox.askyesno('Delete All', 'Are you sure?')

    if confirmation:
        tasks.clear()
        the_cursor.execute('delete from tasks')
        update_task_list()

def clear_task_list():
    task_listbox.delete(0, 'end')

def close_application():
    print(tasks)
    gui_window.destroy()

def retrieve_database():
    tasks.clear()
    for row in the_cursor.execute('select title from tasks'):
        tasks.append(row[0])

if __name__ == "__main__":
    gui_window = tk.Tk()
    gui_window.title("To-Do List")
    gui_window.geometry("400x400+450+250")
    gui_window.resizable(0, 0)
    gui_window.configure(bg="#F99C5D")

    db_connection = sql.connect('listOfTasks.db')
    the_cursor = db_connection.cursor()
    the_cursor.execute('create table if not exists tasks (title text)')

    tasks = []

    header_frame = tk.Frame(gui_window, bg="#F99C5D")
    functions_frame = tk.Frame(gui_window, bg="#F99C5D")
    listbox_frame = tk.Frame(gui_window, bg="#F99C5D")

    header_frame.pack(fill="both")
    functions_frame.pack(side="left", expand=True, fill="both")
    listbox_frame.pack(side="right", expand=True, fill="both")

    header_label = ttk.Label(
        header_frame,
        text="Todo List",
        font=("Freestyle Script", "30"),
        background="#F99C5D",
        foreground="#800000"
    )
    header_label.pack(padx=20, pady=20)

    task_label = ttk.Label(
        functions_frame,
        text="Enter Task:",
        font=("Georgia", "13", "bold"),
        background="#F99C5D",
        foreground="#000000"
    )
    task_label.place(x=30, y=40)

    task_field = ttk.Entry(
        functions_frame,
        font=("Georgia", "12"),
        width=15,
        background="#F99C5D",
        foreground="#A52A2A"
    )
    task_field.place(x=30, y=80)

    add_button = ttk.Button(
        functions_frame,
        text="Add Task",
        width=24,
        command=add_task
    )
    del_button = ttk.Button(
        functions_frame,
        text="Delete Task",
        width=24,
        command=delete_selected_task
    )
    del_all_button = ttk.Button(
        functions_frame,
        text="Delete All Tasks",
        width=24,
        command=delete_all_tasks
    )
    exit_button = ttk.Button(
        functions_frame,
        text="Exit",
        width=24,
        command=close_application
    )

    add_button.place(x=30, y=120)
    del_button.place(x=30, y=160)
    del_all_button.place(x=30, y=200)
    exit_button.place(x=30, y=240)

    task_listbox = tk.Listbox(
        listbox_frame,
        width=23,
        height=13,
        selectmode='SINGLE',
        background="#FFFFFF",
        foreground="#000000",
        selectbackground="#CD853F",
        selectforeground="#FFFFFF"
    )
    task_listbox.place(x=10, y=20)

    retrieve_database()
    update_task_list()

    gui_window.mainloop()

    db_connection.commit()
    the_cursor.close()
