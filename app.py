from genericpath import exists
from flask import Flask, render_template, request, redirect, session
import os
import random
import bcrypt
import psycopg2
import json
import requests
import replace

DATABASE_URL = os.environ.get('DATABASE_URL', 'dbname=moodfood')
SECRET_KEY = os.environ.get('SECRET_KEY', 'this is a pretend secret key')

SEARCH_URL = 'https://api.spoonacular.com/recipes/complexSearch'
RECIPE_URL ='https://api.spoonacular.com/recipes/{id}/information'

API_KEY = 'fdf2c871d7e345309fa9b1aa557e8665'

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
    food = selected_food
    params = {
            'query': food,
            'apiKey': API_KEY,
        }
    response = requests.get(SEARCH_URL, params=params)
    json_data = response.json()
    recipes = json_data['results']
    meal = random.choice(recipes)
    Title = meal["title"]
    Image = meal["image"]
    print(json.dumps(recipes, indent=4))
    print(selected_food)
    print (Title)
    recipe_id = meal['id']
    recipe_response = requests.get(RECIPE_URL.format(id=recipe_id), params=params)
    recipe_json_data = recipe_response.json()
    recipe = recipe_json_data 
    # recipe_instructions=[] 
    x = str(recipe["instructions"])
    y = str(x.strip().split('.'))
    a = str(y.split(','))    
    b = a.replace('<ol>', '')
    c = b.replace('</ol>', '')
    d = c.replace('<li>', '')
    e = d.replace('</li>', '')
    f = e.replace('"', '')
    instructions = f.replace('\\n','')

    # recipe_instructions.append(instructions)

    ingredients = recipe["extendedIngredients"]
    recipe_ingredients = []
    for ingredient in ingredients:
        ingname = ingredient['original']
        recipe_ingredients.append(ingname)
 

    Time = recipe["readyInMinutes"]
    Servings = recipe["servings"]
    print(json.dumps(ingredients, indent=4))
    print(recipe_ingredients)
    print(instructions)
    # return recipes

    return render_template('food.html', instructions = instructions, recipe_ingredients = recipe_ingredients, Time = Time, Servings = Servings, selected_food = selected_food, mood_request = mood_request, Title = Title, Image = Image)

@app.route('/recipe')
def recipe():
    return render_template('recipe.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_action():
    email = request.form.get('email')
    password = request.form.get('password')
    print(email, password)
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE email = %s', [email])
    results = cur.fetchall()
    print(results)
    conn.close()

    if not results:
        return render_template('login.html', message='Cannot find user with this name')
    else:
        password_hash = results[0][4]
        valid = bcrypt.checkpw(password.encode(), password_hash.encode())
        if valid:
            user_name = results[0][1]
            print(f'{user_name}, password valid')
            # session['email'] = email
            user_name = user_name
            session['name'] = user_name
            return redirect('/account')
        else:
            print('invalid')
            return render_template('login.html', message='User not found')

@app.route('/account')
def profile():
  return render_template('account.html')

@app.route('/logout')
def log_out():
  session.clear()
  return redirect('/')
   
@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/create_action', methods=['POST'])
def create_action():
    email = request.form.get('email')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    password = request.form.get('password')
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('SELECT * from users WHERE email=%s', [email])
    email_check = cur.fetchall()
    if email_check:
        reject_email = "There is already an account for this email address. Try logging in"
        return render_template('login.html', reject_email = reject_email)
    else:
        cur.execute('INSERT INTO users (email, firstname, lastname, password) VALUES (%s, %s, %s, %s)', [email, firstname, lastname, password_hash])
    
    conn.commit()
    conn.close()
    print(results)
    def login_action(email):
        email = request.form.get('email')
        password = request.form.get('password')
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE email = %s', [email])
        results = cur.fetchall()
        print(results)
        conn.close()
        password_hash = results[0][4]
        valid = bcrypt.checkpw(password.encode(), password_hash.encode())
        user_name = results[0][1]
        session['email'] = email
        session['name'] = user_name
    login_action(email)
    return redirect('/account')

@app.route('/add_food')
def add_food():
  return render_template('add.html')

@app.route('/add_food_action', methods=['POST'])
def add_food_action():
    food = request.form.get('name')
    mood = request.form.get('mood')
    print(food,mood)
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('SELECT * FROM food WHERE name=%s', [food])
    food_check = cur.fetchall()
    if food_check:
        cur.execute('SELECT * FROM food WHERE mood = %s', [mood])
        mood_check = cur.fetchall()
        reject_message = "This food already exists with this mood"
        if mood_check:
            return render_template('account.html', reject_message=reject_message)
    else:
        cur.execute('INSERT INTO food (name, mood) VALUES (%s, %s)', [food, mood])
    
    conn.commit()
    conn.close()
    success_message = "Success! Your food was added"
    return render_template ('account.html', success_message=success_message)



if __name__ == "__main__":
    app.run(debug=True)