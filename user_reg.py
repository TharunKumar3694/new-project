"""
# User Registration System Demo Project


users = {}


def register_user():
    print("\n===== USER REGISTRATION =====")
    full_name = input("Enter Full Name: ")
    email = input("Enter Email: ")
    mobile = input("Enter Mobile Number: ")
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    confirm_password = input("Confirm Password: ")

    # Validation
    if full_name == "":
        print("Name is required.")

    elif email == "":
        print("Email is required.")

    elif "@" not in email or "." not in email:
        print("Invalid email address.")

    elif mobile == "":
        print("Mobile number is required.")

    elif len(mobile) != 10 or not mobile.isdigit():
        print("Invalid mobile number.")

    elif username == "":
        print("Username is required.")

    elif username in users:
        print("Username already exists.")

    elif password == "":
        print("Password is required.")

    elif password != confirm_password:
        print("Passwords do not match.")

    else:
        users[username] = {
            "Full Name": full_name,
            "Email": email,
            "Mobile": mobile,
            "Password": password
        }

        print("\nRegistration Successful.")
        print("User account created successfully.")
        print("The user can now log in using the registered username and password.")

        print("\nRegistered User Details:")
        print("Name     :", users[username]["Full Name"])
        print("Email    :", users[username]["Email"])
        print("Mobile   :", users[username]["Mobile"])
        print("Username :", username)

register_user()

def login_user():
    print("\n===== USER LOGIN =====")
    login_username = input("Enter Username: ")
    login_password = input("Enter Password: ")

    if login_username in users and users[login_username]["Password"] == login_password:
        print("\nLogin Successful!")
        print("Welcome", users[login_username]["Full Name"])
    else:
        print("Invalid username or password.")


while True:
    print("\n===== MAIN MENU =====")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        register_user()
    elif choice == "2":
        if users:
            login_user()
        else:
            print("No registered users yet. Please register first.")
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid option. Please choose 1, 2, or 3.")

"""

from fastapi import FastAPI
from pydantic import BaseModel
import pymysql
import re

app = FastAPI(
    title="User Registration API",
    version="1.0"
)

# -------------------- MySQL Connection --------------------

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="Tharun@123",
    database="registration_db"
)

cursor = connection.cursor()

# -------------------- Models --------------------

class User(BaseModel):
    full_name: str
    email: str
    mobile: str
    username: str
    password: str
    confirm_password: str


class Login(BaseModel):
    username: str
    password: str


# -------------------- Home API --------------------

@app.get("/")
def get_all_users():

    query = "SELECT id, full_name, email, mobile, username FROM users"
    cursor.execute(query)

    users = cursor.fetchall()

    data = []

    for user in users:
        data.append({
            "id": user[0],
            "full_name": user[1],
            "email": user[2],
            "mobile": user[3],
            "username": user[4]
        })

    return {
        "message": "All Registered Users",
        "users": data
    }


# -------------------- Register API --------------------

@app.post("/register")
def register(user: User):

    # Name Validation
    if user.full_name.strip() == "":
        return {"message": "Name is required"}

    # Email Validation
    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    if not re.match(email_pattern, user.email):
        return {"message": "Invalid email address"}

    # Mobile Validation
    if len(user.mobile) != 10 or not user.mobile.isdigit():
        return {"message": "Invalid mobile number"}

    # Username Validation
    if user.username.strip() == "":
        return {"message": "Username is required"}

    # Check Username Exists
    sql = "SELECT * FROM users WHERE username=%s"
    cursor.execute(sql, (user.username,))
    result = cursor.fetchone()

    if result:
        return {"message": "Username already exists"}

    # Password Validation
    if user.password == "":
        return {"message": "Password is required"}

    if user.password != user.confirm_password:
        return {"message": "Passwords do not match"}

    # Save User
    insert_query = """
    INSERT INTO users
    (full_name, email, mobile, username, password)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        user.full_name,
        user.email,
        user.mobile,
        user.username,
        user.password
    )

    cursor.execute(insert_query, values)
    connection.commit()

    return {
        "message": "User account created successfully."
    }


# -------------------- Login API --------------------

@app.post("/login")
def login(user: Login):

    query = "SELECT * FROM users WHERE username=%s"
    cursor.execute(query, (user.username,))
    result = cursor.fetchone()

    if result is None:
        return {
            "message": "Username not found"
        }

    
    db_password = result[5]

    if user.password != db_password:
        return {
            "message": "Invalid password"
        }

    return {
        "message": "Login Successful",
        "full_name": result[1],
        "username": result[4]
    }