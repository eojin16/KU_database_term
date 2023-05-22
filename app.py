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


@app.route('/register', methods=['post'])
def register():
    global ID
    ID = request.form["id"]
    id = request.form["id"]
    password = request.form["password"]
    send = request.form["send"]
       
    # Login
    if send == "login":
        # Check if a tuple with matching ID, PW already exists
        cur.execute("SELECT * FROM users WHERE id = %s AND password = %s;", (id, password))
        users_result = cur.fetchone()
        print(users_result) # ('admin', '0000')
        
        cur.execute("SELECT * FROM account WHERE id = %s;", (id,))
        account_result = cur.fetchone() # ('admin', 10000000, 'gold', 'tutor')
        print(account_result[3])
        role = account_result[3]
        
        cur.execute("SELECT * FROM lecture;")
        lecture_result = cur.fetchall() # [('00', 'korean history', 1000, 'admin'), ('01', 'database system', 2000, 'admin'), ('02', 'japanese culture', 1500, 'aaa')]
        print(lecture_result)
        
        cur.execute("SELECT e.lecture_name, s.subject_name, e.tutor, COUNT(*) AS number_of_enrollments FROM enrollment e INNER JOIN subject s ON e.code = s.code GROUP BY e.lecture_name, s.subject_name, e.tutor ORDER BY COUNT(*) DESC LIMIT 1;")
        popular_lecture_result = cur.fetchone() # ('database system', 'mathematics', 'admin', 2)
        print(popular_lecture_result)
        
        cur.execute("SELECT * FROM enrollment WHERE tutee = %s;", (id,))
        enrollment_result = cur.fetchall() # [('aa', 'admin', '01', 'database system', 2000)
        print(enrollment_result)
        
        
        print(id)

        # Login fail if no match id
        if users_result is None:
            return render_template("login_fail.html")

        # admin page
        elif id == "admin":
            return render_template("main_basic_admin.html", account=account_result, lecture=lecture_result, popular_lecture=popular_lecture_result)

        # normal user page
        else:
            # tutor page
            if account_result[3] == "tutor":
                return render_template("main_basic_tutor.html", account=account_result, lecture=lecture_result, popular_lecture=popular_lecture_result)

            # tutee page            
            elif account_result[3] == "tutee":
                return render_template("main_basic_tutee.html", account=account_result, lecture=lecture_result, popular_lecture=popular_lecture_result, enrollment=enrollment_result)

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
    cur.execute("INSERT INTO account VALUES (%s, %s, %s, %s);", (id, 10000, initial_rate, role))
    connect.commit()
        
    return render_template("welcome.html")


@app.route('/print_user_table', methods=['post'])
def print_user_table():
    cur.execute("SELECT * FROM users;")
    result = cur.fetchall()
    return render_template("print_user_table.html", users=result)


@app.route('/print_lecture_table', methods=['post'])
def print_lecture_table():
    cur.execute("SELECT * FROM lecture;")
    result = cur.fetchall()
    return render_template("print_lecture_table.html", lecture=result)


@app.route('/my_info_tutee', methods=['post'])
def my_info_tutee():
    my_id = ID
    cur.execute("SELECT * FROM enrollment WHERE tutee = %s;", (my_id,))
    result = cur.fetchall() # [('aa', 'admin', '01', 'database system', 2000)
    print(result)
    return render_template("main_tutee.html", enrollment=result)

@app.route('/my_info_tutor', methods=['post'])
def my_info_tutor():
    my_id = ID
    print(my_id)
    
    # lecture that tutor teaches
    cur.execute("SELECT * FROM enrollment WHERE tutor= %s;", (my_id,))
    my_result = cur.fetchall() # [('aa', 'admin', '01', 'database system', 2000)
    print(my_result)
    
    # lecture that tutor bought
    cur.execute("SELECT * FROM enrollment WHERE tutee= %s;", (my_id,))
    registered_result = cur.fetchall() # [('aa', 'admin', '01', 'database system', 2000)
    print(registered_result)
       
    return render_template("main_tutor.html", my=my_result, registered=registered_result)


if __name__ == '__main__':
    app.run(debug=True)

