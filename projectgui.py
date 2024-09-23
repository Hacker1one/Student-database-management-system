import sqlite3
import tkinter as tk
from tkinter import messagebox
import bcrypt

conn = sqlite3.connect('student_data.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS student_data
                (name TEXT, ID INTEGER, email TEXT, password TEXT)''')

def add_data():
    add_window = tk.Toplevel(root)
    add_window.title("Add Data")

    add_all_button = tk.Button(add_window, text="Add All Data", command=add_all_data)
    add_all_button.pack()

    add_specific_button = tk.Button(add_window, text="Add Specific Data", command=add_specific_data)
    add_specific_button.pack()

def add_all_data():
    def add_data():
        name = name_entry.get()
        ID = int(id_entry.get())
        email = email_entry.get()
        password = pass_entry.get()
        if password == '':
            messagebox.showinfo("Error", "You should add a password.")
            return
        if name == '' or ID == '' or email == '':
            messagebox.showinfo("Error", "Please enter all data.")
            return
        password_bytes = password.encode('utf-8')
        hashpassword = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        hashpassword_str = hashpassword.decode('utf-8')

        cursor.execute("INSERT INTO student_data (name, ID, email, password) VALUES (?, ?, ?, ?)",
                       (name, ID, email, hashpassword_str))
        conn.commit()
        messagebox.showinfo("Success", "All data was added successfully.")
        add_window.destroy()
        
    add_window = tk.Toplevel(root)
    add_window.title("Add All Data")

    name_label = tk.Label(add_window, text="Name:")
    name_label.pack()
    name_entry = tk.Entry(add_window)
    name_entry.pack()

    id_label = tk.Label(add_window, text="ID:")
    id_label.pack()
    id_entry = tk.Entry(add_window)
    id_entry.pack()

    email_label = tk.Label(add_window, text="Email:")
    email_label.pack()
    email_entry = tk.Entry(add_window)
    email_entry.pack()

    pass_label = tk.Label(add_window, text="Password:")
    pass_label.pack()
    pass_entry = tk.Entry(add_window, show='*')
    pass_entry.pack()

    submit_button = tk.Button(add_window, text="Submit", command=add_data)
    submit_button.pack()

def add_specific_data():
    def add_data():
        name = name_entry.get()
        ID = int(id_entry.get())
        email = email_entry.get()
        password = pass_entry.get()
        if password == '':
            messagebox.showinfo("Error", "You should add a password.")
            return
        password_bytes = password.encode('utf-8')
        hashpassword = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        hashpassword_str = hashpassword.decode('utf-8')

        if name == '' and ID == '' and email == '':
            messagebox.showinfo("Error", "Please enter at least one data.")
            return

        cursor.execute("INSERT INTO student_data (name, ID, email, password) VALUES (?, ?, ?, ?)",
                       (name, ID, email, hashpassword_str))
        conn.commit()
        messagebox.showinfo("Success", "Data was added successfully.")
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("Add Specific Data")

    name_label = tk.Label(add_window, text="Name:")
    name_label.pack()
    name_entry = tk.Entry(add_window)
    name_entry.pack()

    id_label = tk.Label(add_window, text="ID:")
    id_label.pack()
    id_entry = tk.Entry(add_window)
    id_entry.pack()

    email_label = tk.Label(add_window, text="Email:")
    email_label.pack()
    email_entry = tk.Entry(add_window)
    email_entry.pack()

    pass_label = tk.Label(add_window, text="Password:")
    pass_label.pack()
    pass_entry = tk.Entry(add_window, show='*')
    pass_entry.pack()

    submit_button = tk.Button(add_window, text="Submit", command=add_data)
    submit_button.pack()

def search(data):
    search_window = tk.Toplevel(root)
    search_window.title("Search")
    result = None

    def perform_search():
        nonlocal result
        if data.lower() == "id":
            ID = int(id_entry.get())
            cursor.execute("SELECT * FROM student_data WHERE ID = ?", (ID,))
            result = cursor.fetchone()
        elif data.lower() == "name":
            name = name_entry.get()
            cursor.execute("SELECT * FROM student_data WHERE name = ?", (name,))
            result = cursor.fetchone()
        elif data.lower() == "email":
            email = email_entry.get()
            cursor.execute("SELECT * FROM student_data WHERE email = ?", (email,))
            result = cursor.fetchone()
        search_window.destroy()

    if data.lower() == "id":
        id_label = tk.Label(search_window, text="Enter the ID:")
        id_label.pack()
        id_entry = tk.Entry(search_window)
        id_entry.pack()
    elif data.lower() == "name":
        name_label = tk.Label(search_window, text="Enter the name:")
        name_label.pack()
        name_entry = tk.Entry(search_window)
        name_entry.pack()
    elif data.lower() == "email":
        email_label = tk.Label(search_window, text="Enter the email:")
        email_label.pack()
        email_entry = tk.Entry(search_window)
        email_entry.pack()

    search_button = tk.Button(search_window, text="Search", command=perform_search)
    search_button.pack()

    search_window.wait_window()
    return result

def modify_data():
    modify_window = tk.Toplevel(root)
    modify_window.title("Modify Data")

    data_type_label = tk.Label(modify_window, text="Enter the data you want to search with (ID, Name or email):")
    data_type_entry = tk.Entry(modify_window)
    data_type_label.pack()
    data_type_entry.pack()

    def execute_modification():
        data = data_type_entry.get().capitalize()
        x = search(data)
        if not x:
            messagebox.showerror("Error", f"No data found with {data}.")
            return

        def on_success(x, data):
            modify_window.destroy()
            modify_data_2(x, data)

        check_pass(x, data, on_success)

    search_button = tk.Button(modify_window, text="Search", command=execute_modification)
    search_button.pack()

def modify_data_2(x, data):
    modify_window = tk.Toplevel(root)
    modify_window.title("Modify Data")

    column_label = tk.Label(modify_window, text="Enter the column to modify (name, ID, or email):")
    column_entry = tk.Entry(modify_window)
    column_label.pack()
    column_entry.pack()

    new_value_label = tk.Label(modify_window, text="Enter the new value:")
    new_value_entry = tk.Entry(modify_window)
    new_value_label.pack()
    new_value_entry.pack()

    def execute_modification_2():
        column = column_entry.get().lower()
        if column not in ['name', 'id', 'email']:
            messagebox.showerror("Error", "Invalid column. Please enter 'name', 'ID', or 'email'.")
            return
        value = new_value_entry.get()
        if data == "Name":
            n = 0
        if data == "Id":
            n=1
        if data == "email":
            n =2
        cursor.execute(f"UPDATE student_data SET {column} = ? WHERE {data} = ?", (value, x[n]))    
       
        conn.commit()
        messagebox.showinfo("Success", "Data modified successfully.")
        modify_window.destroy()

    modify_button = tk.Button(modify_window, text="Modify", command=execute_modification_2)
    modify_button.pack()
    
def check_data():
    def search_and_check():
        data = data_type_entry.get().capitalize()
        x = search(data)
        n = 0
        if data == "Name":
            n = 0
        if data == "Id":
                n=1
        if data == "email":
            n =2
        if x:
            messagebox.showinfo("Success", f"The data for {data} '{x[n]}' is: name is {x[0]}, ID is {x[1]}, and email is {x[2]}.")
        else:
            messagebox.showerror("Error", f"The {data} does not exist in the data.")
            check_window.destroy()
        check_window.destroy()
    check_window = tk.Toplevel(root)
    check_window.title("Check Data")

    data_type_label = tk.Label(check_window, text="Enter the data you want to search with (ID, Name or email):")
    data_type_entry = tk.Entry(check_window)
    data_type_label.pack()
    data_type_entry.pack()
    
    search_button = tk.Button(check_window, text="Search", command=search_and_check)
    search_button.pack()

def check_pass(x, data, on_success):
    pass_window = tk.Toplevel(root)
    pass_window.title("Password")

    def verify_password():
        password = pass_entry.get()
        
        if data == "ID" or data == "Id":
            cursor.execute("SELECT password FROM student_data WHERE ID = ?", (x[1],))
        elif data == "Name":
            cursor.execute("SELECT password FROM student_data WHERE name = ?", (x[0],))
        elif data == "Email":
            cursor.execute("SELECT password FROM student_data WHERE email = ?", (x[2],))

        res = cursor.fetchone()

        if res and bcrypt.checkpw(password.encode('utf-8'), res[0].encode('utf-8')):
            messagebox.showinfo("Success", "Password is correct.")
            pass_window.destroy()
            on_success(x, data) 
        else:
            messagebox.showerror("Error", "The password is incorrect.")

    pass_label = tk.Label(pass_window, text="Password:")
    pass_label.pack()
    pass_entry = tk.Entry(pass_window, show='*')
    pass_entry.pack()

    verify_button = tk.Button(pass_window, text="Verify", command=verify_password)
    verify_button.pack()

root = tk.Tk()

root.title("Student Database Management")

add_button = tk.Button(root, text="Add Data", command=add_data)
add_button.pack()

modify_button = tk.Button(root, text="Modify Data", command=modify_data)
modify_button.pack()

check_button = tk.Button(root, text="Check Data", command=check_data)
check_button.pack()

root.mainloop()
