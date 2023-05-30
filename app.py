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
        users_result = cur.fetchone() # ('admin', '0000')
        
        cur.execute("SELECT * FROM account WHERE id = %s;", (id,))
        account_result = cur.fetchone() # ('admin', 10000000, 'gold', 'tutor')
        
        cur.execute("SELECT * FROM lecture;")
        lecture_result = cur.fetchall() # [('00', 'korean history', 1000, 'admin'), ('01', 'database system', 2000, 'admin'), ('02', 'japanese culture', 1500, 'aaa')]
        
        cur.execute("SELECT e.lecture_name, s.subject_name, e.tutor, COUNT(*) AS number_of_enrollments FROM enrollment e INNER JOIN subject s ON e.code = s.code GROUP BY e.lecture_name, s.subject_name, e.tutor ORDER BY COUNT(*) DESC LIMIT 1;")
        popular_lecture_result = cur.fetchone() # ('database system', 'mathematics', 'admin', 2)
        
        cur.execute("SELECT * FROM enrollment WHERE tutee = %s;", (id,))
        enrollment_result = cur.fetchall() # [('aa', 'admin', '01', 'database system', 2000)
        
        cur.execute("SELECT * FROM rating_info;")
        rank_result = cur.fetchall() # [('00', 'korean history', 1000, 'admin'), ('01', 'database system', 2000, 'admin'), ('02', 'japanese culture', 1500, 'aaa')]

        # Login fail if no match id
        if users_result is None:
            return render_template("login_fail.html")

        # admin page
        elif id == "admin":
            return render_template("main_basic_admin.html", account=account_result, lecture=lecture_result, popular_lecture=popular_lecture_result, rank=rank_result)

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

    cur.execute("SELECT distinct subject.subject_name, enrollment.lecture_name, enrollment.tutor, enrollment.lecture_price FROM enrollment JOIN subject ON subject.code = enrollment.code WHERE enrollment.tutee = %s;", (my_id,))
    registered_result = cur.fetchall() # [('aa', 'admin', '01', 'database system', 2000)
    
    return render_template("main_tutee.html", registered=registered_result)


@app.route('/my_info_tutor', methods=['post'])
def my_info_tutor():
    my_id = ID

    # lecture that tutor teaches
    cur.execute("SELECT distinct subject.subject_name, enrollment.lecture_name, enrollment.tutee, enrollment.lecture_price FROM enrollment JOIN subject ON subject.code = enrollment.code WHERE enrollment.tutor = %s;", (my_id,))
    my_result = cur.fetchall() # [('aa', 'admin', '01', 'database system', 2000)
    print(my_result)
    
    # lecture that tutor bought
    cur.execute("SELECT distinct subject.subject_name, enrollment.lecture_name, enrollment.tutor, enrollment.lecture_price FROM enrollment JOIN subject ON subject.code = enrollment.code WHERE enrollment.tutee = %s;", (my_id,))
    registered_result = cur.fetchall() # [('aa', 'admin', '01', 'database system', 2000)
       
    return render_template("main_tutor.html", my=my_result, registered=registered_result)


@app.route('/register_lecture', methods=['post'])
def register_lecture():
    global TOTAL_PRICE
    global DISCOUNT_PRICE
    global FINAL_PRICE
    global LECTURE_TO_PAY
    
    my_id = ID
    lecture = request.form["lecture"]
    LECTURE_TO_PAY = request.form["lecture"]
    
    cur.execute("SELECT * FROM lecture WHERE name = %s;", (lecture,))
    lecture_result = cur.fetchall() # ('00', 'korean history', 1000, 'admin')

    cur.execute("SELECT * FROM account WHERE id = %s;", (my_id,))
    account_result = cur.fetchone() # ('admin', 10000000, 'gold', 'tutor')
    
    cur.execute("SELECT discount FROM rating_info WHERE rating= %s AND condition <= %s;", (account_result[2], account_result[1]))
    d_result = cur.fetchone()
    
    if d_result is None:
        discount_result = 0
    else:
        discount_result = d_result[0]
    
    total_price = lecture_result[0][2] 
    discount_price = lecture_result[0][2] * discount_result / 100
    final_price = lecture_result[0][2] - discount_price
    
    TOTAL_PRICE = lecture_result[0][2] 
    DISCOUNT_PRICE = lecture_result[0][2] * discount_result / 100
    FINAL_PRICE = lecture_result[0][2] - discount_price
    
    return render_template("lecture_payment.html", account=account_result, discount=discount_result, lecture=lecture_result, discount_price=discount_price, final_price=final_price)


@app.route('/payment', methods=['post'])
def payment():
    my_id = ID
    total_price = TOTAL_PRICE
    discount_price = DISCOUNT_PRICE
    final_price = FINAL_PRICE
    lecture_to_pay = LECTURE_TO_PAY # korean history
    
    cur.execute("SELECT * FROM lecture WHERE name = %s;", (lecture_to_pay,))
    lecture_info = cur.fetchone()
    tutor_id = lecture_info[3]
    
    # payment failure
    cur.execute("SELECT * FROM account WHERE id = %s;", (my_id,))
    account_result = cur.fetchone() # ('admin', 10000000, 'gold', 'tutor')
    credit = account_result[1]
    if (credit < total_price):
        return "Payment Failure : Payment amount exceeds your credit"

    if tutor_id == my_id:
        return "Payment Failure : Unable to pay for your own course"
    
    cur.execute("SELECT * FROM enrollment WHERE tutee = %s AND lecture_name = %s", (my_id, lecture_to_pay))
    enrolled_lecture = cur.fetchone()
    if (enrolled_lecture is not None):
        return "Payment Failure : Can't pay again for a course you've already paid for"
    
    # payment success
    cur.execute("UPDATE account SET credit = credit - %s WHERE id = %s;", (final_price, my_id))
    connect.commit()
    cur.execute("UPDATE account SET credit = credit + %s WHERE id = %s;", (total_price, tutor_id))
    connect.commit()
    cur.execute("INSERT INTO enrollment (tutee, tutor, code, lecture_name, lecture_price) VALUES (%s, %s, %s, %s, %s)", (my_id, tutor_id, lecture_info[0], lecture_info[1], lecture_info[2]))
    connect.commit()
    
    # payment success : tutee update
    cur.execute("SELECT credit FROM account WHERE id = %s;", (my_id,))
    my_credit = cur.fetchone()
    cur.execute("SELECT rating FROM rating_info WHERE condition < %s ORDER BY condition DESC;", (my_credit,))
    my_rating = cur.fetchone()
    cur.execute("UPDATE account SET rating = %s WHERE id = %s;", (my_rating, my_id))
    connect.commit()
    
    # payment success : tutor update
    cur.execute("SELECT credit FROM account WHERE id = %s;", (tutor_id,))
    tutor_credit = cur.fetchone()
    cur.execute("SELECT rating FROM rating_info WHERE condition < %s ORDER BY condition DESC;", (tutor_credit,))
    tutor_rating = cur.fetchone()
    cur.execute("UPDATE account SET rating = %s WHERE id = %s;", (tutor_rating, tutor_id))
    connect.commit()
    
    # success result
    cur.execute("SELECT * FROM enrollment WHERE tutee = %s;", (my_id,))
    result = cur.fetchall()
    
    return render_template("print_enrollment_table.html", enrollment=result)


@app.route('/add', methods=['post'])
def add():
    cur.execute("SELECT * FROM subject;")
    result = cur.fetchall()
    
    return render_template("lecture_add.html", subject=result)


@app.route('/add_lecture', methods=['post'])
def add_lecture():
    code = request.form["code"]
    name = request.form["name"]
    price = request.form["price"]
    my_id = ID
    
    cur.execute("SELECT * FROM subject;")
    subject_result = cur.fetchall()
    
    cur.execute("SELECT * FROM lecture WHERE code = %s AND name = %s AND price = %s AND tutor = %s;", (code, name, price, my_id))
    duplicated = cur.fetchone()
    if (duplicated is not None):
        return "Addition Failure : Duplicated lecture exists"
    
    cur.execute("INSERT INTO lecture (code, name, price, tutor) VALUES (%s, %s, %s, %s)", (code, name, price, my_id))
    connect.commit()
    
    return render_template("lecture_add.html", subject=subject_result)


@app.route('/add_subject', methods=['post'])
def add_subject():
    cur.execute("SELECT * FROM subject;")
    result = cur.fetchall()
    
    return render_template("subject_add.html", subject=result)


@app.route('/add_subject_apply', methods=['post'])
def add_subject_apply():
    code = request.form["code"]
    name = request.form["name"]
    
    cur.execute("SELECT * FROM subject;")
    subject_result = cur.fetchall()
    
    # code duplicated
    cur.execute("SELECT * FROM subject WHERE code = %s;", (code,))
    duplicated = cur.fetchone()
    if (duplicated is not None):
        return "Addition Failure : Duplicated subject code exists"

    # name duplicated
    cur.execute("SELECT * FROM subject WHERE subject_name = %s;", (name,))
    duplicated = cur.fetchone()
    if (duplicated is not None):
        return "Addition Failure : Duplicated subject name exists"
        
    cur.execute("INSERT INTO subject (code, subject_name) VALUES (%s, %s)", (code, name))
    connect.commit()
    
    return render_template("subject_add.html", subject=subject_result)


if __name__ == '__main__':
    app.run(debug=True)

