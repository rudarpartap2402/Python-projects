import json
import getpass
import os

###############################
#
#       add account
#
###############################

def new_pass():

    name     = input("Enter Name : ")
    password = getpass.getpass("Enter Password : ")

    data = {
        "name": name,
        "password": password,
        "passwords": {}
    }

    filename = name + ".json"

    if os.path.exists(filename):
        print(" Account already exists! Please login.")
        return

    with open(filename, "w") as f:
        json.dump(data, f)

    print(" Account Created!\n")

    mode = input("Return To Main Menu (yes/no) : ")
    if mode == "yes":
        start()

###############################
#
#       add website password
#
###############################

def add_website(filename):

    with open(filename, "r") as f:
        data = json.load(f)

    website  = input("Enter Website : ")
    username = input("Enter Username : ")
    password = getpass.getpass("Enter Password : ")

    data["passwords"][website] = {
        "username": username,
        "password": password
    }

    with open(filename, "w") as f:
        json.dump(data, f)

    print(" Password Saved!\n")

    mode = input("Return To Main Menu (yes/no) : ")
    if mode == "yes":
        menu(filename)

###############################
#
#       view passwords
#
###############################

def view_pass(filename):

    with open(filename, "r") as f:
        data = json.load(f)

    if data["passwords"]:
        print("\n---- Your Saved Passwords ----")
        for website in data["passwords"]:
            print(f"\nWebsite  : {website}")
            print(f"Username : {data['passwords'][website]['username']}")
            print(f"Password : {data['passwords'][website]['password']}")
        print()
    else:
        print(" No passwords saved yet!\n")

    mode = input("Return To Main Menu (yes/no) : ")
    if mode == "yes":
        menu(filename)

###############################
#
#       delete password
#
###############################

def delete_pass(filename):

    with open(filename, "r") as f:
        data = json.load(f)

    if data["passwords"]:
        print("\n---- Your Saved Passwords ----")
        websites = list(data["passwords"].keys())
        for i, website in enumerate(websites, 1):
            print(f"  {i}. {website}")

        select = int(input("\nEnter number to delete : "))

        if 1 <= select <= len(websites):
            selected_site = websites[select - 1]
            del data["passwords"][selected_site]

            with open(filename, "w") as f:
                json.dump(data, f)

            print(f" {selected_site} deleted successfully!\n")
        else:
            print(" Invalid selection!\n")
    else:
        print(" No passwords saved yet!\n")

    mode = input("Return To Main Menu (yes/no) : ")
    if mode == "yes":
        menu(filename)

###############################
#
#       exit
#
###############################

def exit_out():
    print("\n Goodbye! Stay safe.\n")
    exit()

###############################
#
#       main menu
#
###############################

def menu(filename):
    while True:
        print('''
------------------------------
           Menu
------------------------------
  1. Add New Website Password
  2. View My Passwords
  3. Delete A Password
  4. Exit
------------------------------''')

        mode = int(input("Select A Mode : "))

        if mode == 1:
            add_website(filename)
        elif mode == 2:
            view_pass(filename)
        elif mode == 3:
            delete_pass(filename)
        elif mode == 4:
            exit_out()
        else:
            print(" Invalid option!\n")

###############################
#
#       login
#
###############################

def login():

    name     = input("Enter Name : ")
    password = getpass.getpass("Enter Your Password : ")

    filename = name + ".json"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)

        if password == data["password"]:
            print(" Login Successful!\n")
            menu(filename)
        else:
            print(" Wrong password!")
    else:
        print(" Account not found! Please register first.")

    mode = input("Return To Start (yes/no) : ")
    if mode == "yes":
        start()

###############################
#
#       start
#
###############################

def start():
    print('''
==============================
  Welcome To Password Manager
==============================
  1. Create New Account
  2. Login
  3. Exit
==============================''')

    mode = int(input("Enter : "))

    if mode == 1:
        new_pass()
    elif mode == 2:
        login()
    elif mode == 3:
        exit_out()
    else:
        print("⚠ Invalid option!\n")
        start()

# ── Run ──
start()