import json
import os

def get_remaining(filename , personal , exit):
    with open(filename, "r") as f:
        data = json.load(f)
    total  = data.get("total", 0)
    spent  = sum(r["rent"]   for r in data.get("rent_details", []))
    spent += sum(f["Amount"] for f in data.get("food_details", []))
    spent += sum(t["amount"] for t in data.get("travel_details", []))
    spent += sum(m["amount"] for m in data.get("misc_details", []))
    return total - spent

###############################
#        rent input
###############################
def rent(filename, total):
    date      = input("Enter Today's Date : ")
    room_rent = int(input("Enter Your Rent : "))
    rent_data = {"date": date, "rent": room_rent}

    with open(filename, "r") as f:
        user_data = json.load(f)
    user_data.setdefault("rent_details", []).append(rent_data)
    with open(filename, "w") as f:
        json.dump(user_data, f, indent=4)

    print("Rent Added Successfully!")
    print(f"Remaining Budget : {get_remaining(filename)}")

###############################
#        food input
###############################
def food(filename, total):
    date      = input("Enter Today's Date : ")
    food_name = input("What did You Eat Today : ")
    amount    = int(input("Amount : "))
    food_data = {"date": date, "food": food_name, "Amount": amount}

    with open(filename, "r") as f:
        user_data = json.load(f)
    user_data.setdefault("food_details", []).append(food_data)
    with open(filename, "w") as f:
        json.dump(user_data, f, indent=4)

    print("Data Added Successfully!")
    print(f"Remaining Budget : {get_remaining(filename)}")

###############################
#        travel input
###############################
def travel(filename, total):
    date   = input("Enter Today's Date : ")
    place  = input("Where did You Travel : ")
    amount = int(input("Enter Your Spending : "))
    travel_data = {"date": date, "travel": place, "amount": amount}

    with open(filename, "r") as f:
        user_data = json.load(f)
    user_data.setdefault("travel_details", []).append(travel_data)
    with open(filename, "w") as f:
        json.dump(user_data, f, indent=4)

    print("Data Added Successfully!")
    print(f"Remaining Budget : {get_remaining(filename)}")

###############################
#        misc input
###############################
def misc(filename, total):
    date     = input("Enter Today's Date : ")
    activity = input("Enter Your Misc Activity : ")
    amount   = int(input("Enter Your Amount : "))
    misc_data = {"date": date, "misc": activity, "amount": amount}

    with open(filename, "r") as f:
        user_data = json.load(f)
    user_data.setdefault("misc_details", []).append(misc_data)
    with open(filename, "w") as f:
        json.dump(user_data, f, indent=4)

    print("Data Added Successfully!")
    print(f"Remaining Budget : {get_remaining(filename)}")

###############################
#     personal activity
###############################
def personal(filename, total):
    print('''Select Your Category
1. Rent
2. Food
3. Travel
4. Misc''')
    mode = int(input("Select Your Mode : "))
    if   mode == 1: rent(filename, total)
    elif mode == 2: food(filename, total)
    elif mode == 3: travel(filename, total)
    elif mode == 4: misc(filename, total)
    else: print("Invalid Option")

###############################
#        budget input
###############################
def budget(filename):
    total = int(input("Enter Your Total Budget This Month : "))

    # ✅ READ first — preserves password, name, email
    with open(filename, "r") as f:
        data = json.load(f)

    # ✅ Only update total
    data["total"] = total

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Your This Month Budget Is : {total}")
    personal(filename, total)

###############################
#        sign up
###############################
def sign_up():
    name     = input("Enter Your Name : ")
    password = input("Enter Password : ")        # ✅ string not int
    phone    = input("Enter Your Number : ")
    email    = input("Enter Your E-Mail ID : ")

    filename = name + ".json"

    if os.path.exists(filename):
        print("Account already exists! Please login.")
        return

    data = {
        "name"     : name,
        "phone"    : phone,
        "email"    : email,
        "password" : password,                   # ✅ saved as string
        "total"    : 0,
        "rent_details"  : [],                    # ✅ consistent keys
        "food_details"  : [],
        "travel_details": [],
        "misc_details"  : []
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print("\nAccount Created!\n")
    budget(filename)

###############################
#          login
###############################
def login():
    name     = input("Enter Name : ")
    password = input("Enter Password : ")        # ✅ string not int

    filename = name + ".json"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)

        if password == data["password"]:         # ✅ string comparison
            print("Login Successful!\n")
            total = data.get("total", 0)         # ✅ total passed correctly
            personal(filename, total)
        else:
            print("Wrong password!")
    else:
        print("Account not found! Please register first.")

###############################
#          start
###############################
def start():
    print('''
    Welcome To Your Expense Tracker
      Track Every Expense Easily
    ''')

    print("1. Sign Up\n2. Login\n3. Exit\n")

    while True:                                  # ✅ loop instead of recursion
        try:
            mode = int(input("Enter : "))
            if   mode == 1: sign_up(); break
            elif mode == 2: login();   break
            elif mode == 3: print("Goodbye!"); break
            else: print("Invalid option! Try again.")
        except ValueError:
            print("Please enter a number!")      # ✅ handles letters input

start()