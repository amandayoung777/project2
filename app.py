from flask import Flask, render_template, request, redirect, session
import os
import random

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
    selected_food = random.choice(results[0])
    # selected_food = initial_result.str.replace('(','').replace(')','').replace(',','')
    print(selected_food)
    return render_template('food.html', selected_food = selected_food, mood_request = mood_request)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_action():
    email = request.form.get('email')
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('SELECT id, email, name FROM users WHERE email = %s;', [email])
    results = cur.fetchone()
    
    print(email, 'email')
    print(email == None, 'results')
    conn.commit()
    conn.close()

    if results != None:
        id = results[0]
        email = results[1]
        name = results[2]
        
        if results[1] == email:
            session['id'] = id
            session['name'] = name
            print('yes')
            if id is None:
                print('none')
            else:
                print('hi')
            return redirect('/')
    else:
        print('no')
        return redirect('/login')

@app.route('/logout')
def log_out():
  session.clear()
  return redirect('/')
   






if __name__ == "__main__":
    app.run(debug=True)