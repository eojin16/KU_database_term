import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)
connect = psycopg2.connect(dbname="term", user="postgres", password="postgres")
cur = connect.cursor()  # create cursor

@app.route('/')
def main():
    return render_template("welcome.html")


@app.route('/return', methods=['post'])
def re_turn():
    return render_template("welcome.html")


@app.route('/print_user_table', methods=['post'])
def print_user_table():
    cur.execute("SELECT * FROM users;")
    result = cur.fetchall()
    
    id = request.form.get("id")
    
    if id == "admin":
        return render_template("print_user_table.html", users=result)
    
    else:
        return "You are not authorized to view this page."


@app.route('/register', methods=['post'])
def register():
    id = request.form["id"]
    password = request.form["password"]
    send = request.form["send"]
    
    # Login
    if send == "login":
        # Check if a tuple with matching ID, PW already exists
        cur.execute("SELECT * FROM users WHERE id = %s AND password = %s;", (id, password))
        result = cur.fetchone()

        # Login fail
        if result is None:
            return render_template("login_fail.html")

        # login success
        return render_template("main_basic.html")

    # Sign up
    elif send == "sign up": 
        return render_template("signup.html")
     
@app.route('/create', methods=['post'])
def create():      
    id = request.form["id"]
    password = request.form["password"]
    initial_rate = 'welcome'
    role = request.form["role"]    
      
    # Check if ID already exists
    cur.execute("SELECT * FROM users WHERE id = %s;", (id,))
    result = cur.fetchone()

    # If the ID you're trying to sign up for already exists
    if result is not None:
        return render_template("ID_collision.html")

    # insert user into users table
    cur.execute("INSERT INTO users VALUES (%s, %s);", (id, password))
    connect.commit()
    
    # Insert user into account table
    cur.execute("INSERT INTO account VALUES (%s, %s, %s, %s);", (id, 0, initial_rate, role))
    connect.commit()
        
    return render_template("welcome.html")


if __name__ == '__main__':
    app.run(debug=True)

