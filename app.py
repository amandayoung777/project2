from flask import Flask, render_template, request, redirect, session
import os
import random
import bcrypt
import psycopg2
DATABASE_URL = os.environ.get('DATABASE_URL', 'dbname=moodfood')
SECRET_KEY = os.environ.get('SECRET_KEY', 'this is a pretend secret key')

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
cur.execute('SELECT id, name, mood FROM food')
results = cur.fetchall()
conn.close()
print(results)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mood_action', methods=['POST'])
def mood_action():
    mood_request = request.form.get('mood')
    print(mood_request)
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('SELECT name FROM food WHERE mood=%s;', [mood_request])
    results = cur.fetchall()
    conn.commit()
    conn.close()
    print(results)
    # for result in range(len(results)):
    #     print(results[result], end="")
    # initial_result = random.choice(results)
    selected = random.choice(results)
    initial_result = list(selected)
    selected_food = ''.join(initial_result)
    print(selected_food)
    return render_template('food.html', selected_food = selected_food, mood_request = mood_request)

@app.route('/login')
def login():
    return render_template('login.html')

# @app.route('/login', methods=['POST'])
# def login_action():
#     email = request.form.get('email')
#     password = request.form.get('password')
#     print(f'{email} {password}')
#     conn = psycopg2.connect(DATABASE_URL)
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM users WHERE username = %s', [username])
#     results = cur.fetchall()
#     print(results)
#     conn.close()

#     if not results:
#         return render_template('login.html', message='Cannot find user with this name')
#     else:
#         password_hash = results[0][4]
#         valid = bcrypt.checkpw(password.encode(), password_hash.encode())
#         if valid:
#             user_name = results[0][2]
#             print(f'{user_name}, password valid')
#             session['email'] = email
#             session['name'] = user_name
#             return redirect('/')
#         else:
#             print('invalid')
#             return render_template('login.html', message='User not found')


@app.route('/logout')
def log_out():
  session.clear()
  return redirect('/')
   
@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/create_action', methods=['POST'])
def create_action():
    username = request.form.get('username')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    password = request.form.get('password')
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('INSERT INTO users (username, firstname, lastname, email, password) VALUES (%s, %s, %s, %s, %s)', [username, firstname, lastname, email, password_hash])
    
    conn.commit()
    conn.close()
    print(results)
    return redirect ('/login')




if __name__ == "__main__":
    app.run(debug=True)