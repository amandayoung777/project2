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
    cur.execute('SELECT name FROM food WHERE mood=%s', [mood_request])
    results = cur.fetchall()
    conn.commit()
    conn.close()
    print(results)
    return render_template('food.html', mood_request = mood_request)
   






if __name__ == "__main__":
    app.run(debug=True)