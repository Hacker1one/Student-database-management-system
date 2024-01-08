import sqlite3
import pandas as pd
import bcrypt
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
    ID = input("Enter the ID (Type nothing to skip): ")
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
        'ID': [int(ID)] if ID.isdigit() else [None],
        'email': [email],
        'password': [hashpassword_str]
    }
    df = pd.DataFrame(table_data)
    df.to_sql('student_data', conn, if_exists='append', index=False)

def search(data):
    #data = input("Enter the data you want to search with (ID, Name or email): ").capitalize()
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
    if not check_pass(x[0], data):
        return
    check_pass(x, data)
    column = input("Enter the column to modify (name, ID, or email): ")
    value = input("Enter the new value: ")
    cursor.execute(f"UPDATE student_data SET {column} = ? WHERE {data} = ?", (value, x[0]))
    conn.commit()

def check_data():
    data = input("Enter the data you want to search with (ID, Name or email): ").capitalize()
    x = search(data)
    if x:
        print(f"The data for {data} '{x[1]}' is: {x}.")
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
        cursor.execute("SELECT password FROM student_data WHERE ID = ?", (x,))
        res = cursor.fetchone()
    elif data == "Name":
        cursor.execute("SELECT password FROM student_data WHERE name = ?", (x,))
        res = cursor.fetchone()
    elif data == "Email":
        cursor.execute("SELECT password FROM student_data WHERE email = ?", (x,))
        res = cursor.fetchone() 
    if res and bcrypt.checkpw(password.encode(), res[0]):
        return True
    else:
        print("The password is incorrect")
        return False
    
def your_need():
    while True:
        print("1. Add Data")
        print("2. Modify Data")
        print("3. Check Data")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            add_data()
        elif choice == '2':
            modify_data()
        elif choice == '3':
            check_data()
        else:
            print("Invalid choice. Please enter a valid choice.")

        if not continue1():
            break
    conn.close()

your_need()

