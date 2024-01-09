import sqlite3
import pandas as pd
import bcrypt
import tkinter as tk
from tkinter import messagebox
conn = sqlite3.connect('student_data.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS student_data
                (name TEXT, ID INTEGER, email TEXT, password TEXT)''')
def add_data():
    choice = int(input("Do you want to add all data or just part of it (add 1 for all data, add 2 for part of it): "))
    if choice == 1:
        add_all_data()
    elif choice == 2:
        add_specific_data()
    else:
        print("Invalid choice. Please enter a valid choice.")

def add_all_data():
    name = input("Enter the name: ")
    ID = int(input("Enter the ID: "))
    email = input("Enter the email: ")
    password = input("Enter password: ")
    if password == '':
        print("You should add a password. ")
        return
    password_bytes = password.encode('utf-8')    
    hashpassword = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    hashpassword_str = hashpassword.decode('utf-8')

    cursor.execute("INSERT INTO student_data (name, ID, email, password) VALUES (?, ?, ?, ?)", (name, ID, email, hashpassword_str))
    conn.commit()
    

def add_specific_data():
    print("\nEnter the data you want to add:")
    name = input("Enter the name (Type nothing to skip): ")
    ID = int(input("Enter the ID (Type nothing to skip): "))
    email = input("Enter the email (Type nothing to skip): ")
    password = input("Enter password: ")
    if password == '':
        print("You should add a password. ")
        return
    password_bytes = password.encode('utf-8')    
    hashpassword = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    hashpassword_str = hashpassword.decode('utf-8')

    if name == '' and ID == '' and email == '':
        print("Please enter at least one data.")
        return

    table_data = {
        'name': [name],
        'ID': [ID] ,
        'email': [email],
        'password': [hashpassword_str]
    }
    df = pd.DataFrame(table_data)
    df.to_sql('student_data', conn, if_exists='append', index=False)

def search(data):
    if data == "Id" or data == "ID":
        ID = int(input("Enter the ID: "))
        cursor.execute("SELECT * FROM student_data WHERE ID = ?", (ID,))
        result = cursor.fetchone()
    elif data =="Name":
        name = input("Enter the name: ")
        cursor.execute("SELECT * FROM student_data WHERE name = ?", (name,))
        result = cursor.fetchone()
    elif data =="Email":
        email = input("Enter the email: ")
        cursor.execute("SELECT * FROM student_data WHERE email = ?", (email,))
        result = cursor.fetchone()
    if result:
        return result
    else:
        return None
    
def modify_data():
    data = input("Enter the data you want to search with (ID, Name or email): ").capitalize()
    x = search(data)
    n = 0
    if not check_pass(x, data):
        return
    column = input("Enter the column to modify (name, ID, or email): ").lower()
    if column not in ['name', 'id', 'email']:
        print("Invalid column. you should type (name, ID, or email).")
        return
    value = input("Enter the new value: ")
    if data == "Name":
        n = 0
    if data == "Id":
        n=1
    if data == "email":
        n =2
    cursor.execute(f"UPDATE student_data SET {column} = ? WHERE {data} = ?", (value, x[n]))    
    conn.commit()

def check_data():
    data = input("Enter the data you want to search with (ID, Name or email): ").capitalize()
    x = search(data)
    n=0
    if data == "Name":
        n = 0
    if data == "Id":
        n=1
    if data == "email":
        n =2
    if x:
        print(f"The data for {data} '{x[n]}' is: {(x[0], x[1], x[2])}.")
    else:
        print(f"The {data} does not exist in the data.")

def continue1():
    while True:
        choice = input("Do you want to continue (Y for yes, N for No): ").capitalize()
        if choice == "Y":
            return True
        elif choice == "N":
            return False
        else:
            print("Invalid choice. Please enter Y or N.")

def check_pass(x, data):
    password = input("Enter your password: ")
    if data == "ID" or data == "Id":
        cursor.execute("SELECT password FROM student_data WHERE ID = ?", (x[1],))
        res = cursor.fetchone()
    elif data == "Name":
        cursor.execute("SELECT password FROM student_data WHERE name = ?", (x[0],))
        res = cursor.fetchone()
    elif data == "Email":
        cursor.execute("SELECT password FROM student_data WHERE email = ?", (x[2],))
        res = cursor.fetchone() 
    if bcrypt.checkpw(password.encode('utf-8'), res[0].encode('utf-8')):
        return True
    else:
        print("The password is incorrect")
        return False
    
# def your_need():
#     while True:
#         print("1. Add Data")
#         print("2. Modify Data")
#         print("3. Check Data")
#         choice = input("Enter your choice: ")
#         if choice == '1':
#             add_data()
#         elif choice == '2':
#             modify_data()
#         elif choice == '3':
#             check_data()
#         else:
#             print("Invalid choice. Please enter a valid choice.")
            
#         if not continue1():
#             break
#     conn.close()

# your_need()

def main_gui():
    root = tk.Tk()
    root.title("Student Database")

    def add_all_gui():
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
        
        email_label = tk.Label(add_window, text="Name:")
        email_label.pack()
        email_entry = tk.Entry(add_window)
        email_entry.pack()
        
        pass_label = tk.Label(add_window, text="Name:")
        pass_label.pack()
        pass_entry = tk.Entry(add_window, show='*')
        pass_entry.pack()

        submit_button = tk.Button(add_window, text="Submit", command=add_all_data)
        submit_button.pack()
        
        messagebox.showinfo("Success", "Data added successfully.")
        add_window.destroy()

    def add_specific_gui():
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
        
        email_label = tk.Label(add_window, text="Name:")
        email_label.pack()
        email_entry = tk.Entry(add_window)
        email_entry.pack()
        
        pass_label = tk.Label(add_window, text="Name:")
        pass_label.pack()
        pass_entry = tk.Entry(add_window, show='*')
        pass_entry.pack()

        submit_button = tk.Button(add_window, text="Submit", command=add_specific_data)
        submit_button.pack()
        
        messagebox.showinfo("Success", "Data added successfully.")
        add_window.destroy()

    def modify_gui():
        def search_and_modify():
            data = data_type_entry.get().capitalize()
            x = search(data)
            n = 0
            if not check_pass(x, data):
                return
            column = column_entry.get().lower()
            if column not in ['name', 'id', 'email']:
                messagebox.showerror("Error", "Invalid column. Please enter 'name', 'ID', or 'email'.")
                return
            value = new_value_entry.get()
            if data == "Name":
                n = 0
            elif data == "Id":
                n = 1
            elif data == "Email":
                n = 2
            cursor.execute(f"UPDATE student_data SET {column} = ? WHERE {data} = ?", (value, x[n]))    
            conn.commit()
            messagebox.showinfo("Success", "Data modified successfully.")
            modify_window.destroy()

        modify_window = tk.Toplevel(root)
        modify_window.title("Modify Data")

        data_type_label = tk.Label(modify_window, text="Enter the data type (ID, Name, or Email):")
        data_type_entry = tk.Entry(modify_window)
        data_type_label.pack()
        data_type_entry.pack()

        column_label = tk.Label(modify_window, text="Enter the column to modify (name, ID, or email):")
        column_entry = tk.Entry(modify_window)
        column_label.pack()
        column_entry.pack()

        new_value_label = tk.Label(modify_window, text="Enter the new value:")
        new_value_entry = tk.Entry(modify_window)
        new_value_label.pack()
        new_value_entry.pack()

        search_button = tk.Button(modify_window, text="Modify", command=search_and_modify)
        search_button.pack()

    def check_gui():
        def search_and_check():
            data = data_type_entry.get().capitalize()
            x = search(data)
            n = 0
            if x:
                messagebox.showinfo("Success", f"The data for {data} '{x[n]}' is: {(x[0], x[1], x[2])}.")
            else:
                messagebox.showerror("Error", f"The {data} does not exist in the data.")
            check_window.destroy()

        check_window = tk.Toplevel(root)
        check_window.title("Check Data")

        data_type_label = tk.Label(check_window, text="Enter the data type (ID, Name, or Email):")
        data_type_entry = tk.Entry(check_window)
        data_type_label.pack()
        data_type_entry.pack()

        search_button = tk.Button(check_window, text="Search", command=search_and_check)
        search_button.pack()
   
    add_button = tk.Button(root, text="Add Data", command=add_all_gui)
    add_button.pack()

    specific_button = tk.Button(root, text="Add Specific Data", command=add_specific_gui)
    specific_button.pack()

    modify_button = tk.Button(root, text="Modify Data", command=modify_gui)
    modify_button.pack()

    check_button = tk.Button(root, text="Check Data", command=check_gui)
    check_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main_gui()