from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg
import json

app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────────
#           DATABASE CONNECTION
# ─────────────────────────────────────────

def get_conn():
    return psycopg.connect(
        dbname="postgres",
        user="postgres",
        password="Rudar(2402)",
        host="localhost",
        port=5432
    )

# ─────────────────────────────────────────
#           HELPER — GET REMAINING BUDGET
# ─────────────────────────────────────────

def get_remaining(name):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT total, rent_details, food_details, travel_details, misc_details FROM users WHERE name = %s",
        (name,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return 0

    total          = row[0]
    rent_details   = row[1] or []
    food_details   = row[2] or []
    travel_details = row[3] or []
    misc_details   = row[4] or []

    spent  = sum(r["rent"]   for r in rent_details)
    spent += sum(f["Amount"] for f in food_details)
    spent += sum(t["amount"] for t in travel_details)
    spent += sum(m["amount"] for m in misc_details)

    return total - spent

# ─────────────────────────────────────────
#           SIGN UP
# ─────────────────────────────────────────

@app.route("/signup", methods=["POST"])
def sign_up():
    body     = request.get_json()
    name     = body.get("name")
    password = body.get("password")
    phone    = body.get("phone")
    email    = body.get("email")

    if not all([name, password, phone, email]):
        return jsonify({"error": "All fields are required"}), 400

    try:
        conn   = get_conn()
        cursor = conn.cursor()

        # check if user already exists
        cursor.execute("SELECT name FROM users WHERE name = %s", (name,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"error": "Account already exists! Please login."}), 409

        # insert new user
        cursor.execute(
            "INSERT INTO users (name, password, phone, email) VALUES (%s, %s, %s, %s)",
            (name, password, phone, email)
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Account created successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────
#           LOGIN
# ─────────────────────────────────────────

@app.route("/login", methods=["POST"])
def login():
    body     = request.get_json()
    name     = body.get("name")
    password = body.get("password")

    try:
        conn   = get_conn()
        cursor = conn.cursor()

        cursor.execute("SELECT password, total FROM users WHERE name = %s", (name,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return jsonify({"error": "Account not found! Please register first."}), 404

        if password != row[0]:
            return jsonify({"error": "Wrong password!"}), 401

        return jsonify({
            "message"  : "Login successful!",
            "name"     : name,
            "total"    : row[1],
            "remaining": get_remaining(name)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────
#           SET BUDGET
# ─────────────────────────────────────────

@app.route("/budget", methods=["POST"])
def set_budget():
    body  = request.get_json()
    name  = body.get("name")
    total = body.get("total")

    if not name or total is None:
        return jsonify({"error": "name and total are required"}), 400

    try:
        conn   = get_conn()
        cursor = conn.cursor()

        cursor.execute("UPDATE users SET total = %s WHERE name = %s", (total, name))
        conn.commit()
        conn.close()

        return jsonify({
            "message": "Budget updated successfully!",
            "total"  : total
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────
#           ADD RENT
# ─────────────────────────────────────────

@app.route("/expense/rent", methods=["POST"])
def add_rent():
    body      = request.get_json()
    name      = body.get("name")
    date      = body.get("date")
    room_rent = body.get("rent")

    if not all([name, date, room_rent]):
        return jsonify({"error": "name, date and rent are required"}), 400

    try:
        conn   = get_conn()
        cursor = conn.cursor()

        new_entry = json.dumps([{"date": date, "rent": room_rent}])

        cursor.execute(
            "UPDATE users SET rent_details = rent_details || %s::jsonb WHERE name = %s",
            (new_entry, name)
        )
        conn.commit()
        conn.close()

        return jsonify({
            "message"  : "Rent added successfully!",
            "remaining": get_remaining(name)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────
#           ADD FOOD
# ─────────────────────────────────────────

@app.route("/expense/food", methods=["POST"])
def add_food():
    body      = request.get_json()
    name      = body.get("name")
    date      = body.get("date")
    food_name = body.get("food")
    amount    = body.get("amount")

    if not all([name, date, food_name, amount]):
        return jsonify({"error": "name, date, food and amount are required"}), 400

    try:
        conn   = get_conn()
        cursor = conn.cursor()

        new_entry = json.dumps([{"date": date, "food": food_name, "Amount": amount}])

        cursor.execute(
            "UPDATE users SET food_details = food_details || %s::jsonb WHERE name = %s",
            (new_entry, name)
        )
        conn.commit()
        conn.close()

        return jsonify({
            "message"  : "Food expense added successfully!",
            "remaining": get_remaining(name)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────
#           ADD TRAVEL
# ─────────────────────────────────────────

@app.route("/expense/travel", methods=["POST"])
def add_travel():
    body   = request.get_json()
    name   = body.get("name")
    date   = body.get("date")
    place  = body.get("travel")
    amount = body.get("amount")

    if not all([name, date, place, amount]):
        return jsonify({"error": "name, date, travel and amount are required"}), 400

    try:
        conn   = get_conn()
        cursor = conn.cursor()

        new_entry = json.dumps([{"date": date, "travel": place, "amount": amount}])

        cursor.execute(
            "UPDATE users SET travel_details = travel_details || %s::jsonb WHERE name = %s",
            (new_entry, name)
        )
        conn.commit()
        conn.close()

        return jsonify({
            "message"  : "Travel expense added successfully!",
            "remaining": get_remaining(name)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────
#           ADD MISC
# ─────────────────────────────────────────

@app.route("/expense/misc", methods=["POST"])
def add_misc():
    body     = request.get_json()
    name     = body.get("name")
    date     = body.get("date")
    activity = body.get("misc")
    amount   = body.get("amount")

    if not all([name, date, activity, amount]):
        return jsonify({"error": "name, date, misc and amount are required"}), 400

    try:
        conn   = get_conn()
        cursor = conn.cursor()

        new_entry = json.dumps([{"date": date, "misc": activity, "amount": amount}])

        cursor.execute(
            "UPDATE users SET misc_details = misc_details || %s::jsonb WHERE name = %s",
            (new_entry, name)
        )
        conn.commit()
        conn.close()

        return jsonify({
            "message"  : "Misc expense added successfully!",
            "remaining": get_remaining(name)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────
#           DASHBOARD — VIEW ALL EXPENSES
# ─────────────────────────────────────────

@app.route("/dashboard/<name>", methods=["GET"])
def dashboard(name):
    try:
        conn   = get_conn()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name, total, rent_details, food_details, travel_details, misc_details FROM users WHERE name = %s",
            (name,)
        )
        row = cursor.fetchone()
        conn.close()

        if not row:
            return jsonify({"error": "Account not found!"}), 404

        return jsonify({
            "name"          : row[0],
            "total_budget"  : row[1],
            "remaining"     : get_remaining(name),
            "rent_details"  : row[2] or [],
            "food_details"  : row[3] or [],
            "travel_details": row[4] or [],
            "misc_details"  : row[5] or []
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
