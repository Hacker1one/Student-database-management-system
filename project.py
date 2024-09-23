import sqlite3
import bcrypt
conn = sqlite3.connect('student_data.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS student_data
                (name TEXT, ID INTEGER, email TEXT, password TEXT)''')
def add_data():
    choice = input_type_error("Do you want to add all data or just part of it (add 1 for all data, add 2 for part of it): ")
    if choice == 1:
        add_all_data()
    elif choice == 2:
        add_specific_data()
    else:
        print("Invalid choice. Please enter a valid choice.")
        
def add_all_data():
    name = input("Enter the name: ")
    if name == '':
            print("Error", "Please enter the name.")
            return
    ID = input_type_error("Enter the ID: ")
    if ID == '':
            print("Error", "Please enter the ID.")
            return
    email = input("Enter the email: ")
    if email == '':
            print("Error", "Please enter the email.")
            return
    password = input("Enter password: ")
    if password == '':
        print("You should add a password. ")
        return
    
    password_bytes = password.encode('utf-8')    
    hashpassword = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    hashpassword_str = hashpassword.decode('utf-8')

    cursor.execute("INSERT INTO student_data (name, ID, email, password) VALUES (?, ?, ?, ?)",(name, ID, email, hashpassword_str))
    conn.commit()
    
def add_specific_data():
    print("\nEnter the data you want to add:")
    name = input("Enter the name (Type nothing to skip): ")
    ID = input_type_error("Enter the ID (Type nothing to skip): ")
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

    cursor.execute("INSERT INTO student_data (name, ID, email, password) VALUES (?, ?, ?, ?)",(name, ID, email, hashpassword_str))
    conn.commit()
    
def search(data):
    if data == "Id" or data == "ID":
        ID = input_type_error("Enter the ID: ")
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
    data = input_type_error2("Enter the data you want to search with (ID, Name or email): ")
    x = search(data)
    if x is None:
        print(f"There is no data associated with this {data}")
        return
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
    data = input_type_error2("Enter the data you want to search with (Name, ID, or email): ")
    x = search(data)
    if x is None:
        print(f"There is no data associated with this {data}")
        return
    n=0
    if data == "Name":
        n = 0
    if data == "Id":
        n=1
    if data == "email":
        n =2
    if x:
        print(f"The data for {data} '{x[n]}' is: name is {x[0]}, ID is {x[1]}, and email is {x[2]}.")
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

def input_type_error(num):
    while True:
        ID = input(num)
        if ID == "":
            return ID
        else:
            try:
                ID = int(ID)
                return ID
            except ValueError:
                print("Please add the ID as numbers.")

def input_type_error2(x):
    while True:
        try:
            data = input(x).capitalize()
            if data in ["Id", "Name", "Email"]:
                return data
            else:
                print(f"Invalid data. Please choose from (Name, ID, or Email).")
        except ValueError:
            print("Invalid input. Please try again.")
  
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

