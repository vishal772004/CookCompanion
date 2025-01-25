import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session,jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import requests
from functools import wraps

# Configure application
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


API_KEY ="71e8180df6d448beb28ce616cc667957"
# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///recipes.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    if request.method=="POST":
        session.clear()

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if( len(rows)!=1 ):
            flash("User doesn't exists, Please Register!")
            return render_template("register.html")
        if(not check_password_hash(rows[0]['password'],request.form.get('password'))):
            flash("Incorrect Password, Please try again!")
            return render_template("login.html")
        session["user_id"] = rows[0]["id"]

        return redirect("/home")

@app.route("/")
@app.route("/home",methods=["GET","POST"])
@login_required
def home():
    if request.method=="GET":
            cuisines = [
    "African", "American", "British", "Cajun", "Caribbean", "Chinese",
    "Eastern European", "European", "French", "German", "Greek", "Indian",
    "Irish", "Italian", "Japanese", "Jewish", "Korean", "Latin American",
    "Mediterranean", "Mexican", "Middle Eastern", "Nordic", "Southern",
    "Spanish", "Thai", "Vietnamese"]
            allergies = ["Egg-Free","Gluten","Peanut","Sesame",
     "Seafood","Shellfish","Soy","Sulfite","Tree Nut","Wheat","Vegetarian","Vegan",
     "Pescetarian","Ketogenic","Paleo","Whole30","Low FODMAP","No Added Sugar",
     "Dairy-Free","Gluten-Free","Nut-Free","Soy-Free","Sugar-Conscious","Wheat-Free"]
            dietlabels = ["Vegetarian","Vegan","Pescetarian","Ketogenic","Paleo",
    "Whole30","Low FODMAP","Gluten-Free","Dairy-Free","Lacto-Vegetarian","Ovo-Vegetarian",
    "Paleo-Vegetarian","High-Protein","Low-Carb","Low-Fat","Sugar-Conscious"]
            get_recipes()
            return render_template("home.html" ,  cuisines=cuisines,allergies=allergies,dietlabels=dietlabels)
    if request.method=="POST":
        cuisines=request.form.get("cuisines_")
        allergies=request.form.get("allergy_")
        dietlabels=request.form.get("dietlabel_")
        dish_type = request.form.get("dish_type")
        ingredients = request.form.get("ingredient")
        print(cuisines)
        return render_template("result.html")





@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        print("Check1")
        password = request.form.get("password")
        checks=0
        username = request.form.get("username")
        users = db.execute("SELECT username FROM users")
        usercheck = [sublist[d] for sublist in users for d in sublist if 'username' in d]
        if not username :
            flash("Enter the Username")
            return render_template ("register.html")

        if not password or len(password) <6 or not password.isalnum():
            flash("Enter the Password with minimum 6 characters and no special characters")
            return render_template ("register.html")

        if request.form.get("password")==request.form.get("confirmation"):
            checks+=1
        else:
            flash("Enter the correct password")
            return render_template ("register.html")

        password_hash = generate_password_hash(password, method='pbkdf2', salt_length=16)

        if username in usercheck:
            flash("Username already exists")
            return render_template("register.html")
        try:
            db.execute("INSERT INTO users (username,password) values (?,?)",username,password_hash)
        except:
            flash("Enter the details correctly")
            return render_template("register.html")
        print("Check4")
        flash("User registered successfully")
        return render_template("login.html")




@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route('/get_recipes', methods=["POST"])
@login_required
def get_recipes():
    SPOONACULAR_API_URL = "https://api.spoonacular.com/recipes/complexSearch"
    if request.method=="POST":

        allergies = request.form.getlist('allergies')
        diets = request.form.getlist('dietlabels')
        cuisines = request.form.getlist('cuisines')
        ingredients = request.form.getlist('ingredient[]')
        dish_type = request.form.getlist('dish_type')
        print(allergies,diets, cuisines,ingredients,dish_type)

        params = {
            'apiKey': API_KEY,
            'includeIngredients': ingredients if ingredients else None,
            'diet': diets if diets else None,
            'cuisine': cuisines if cuisines else None,
            'number': 12,
            'intolerances':allergies if allergies else None,
            'type':dish_type if dish_type else None,

        }


        try:

            response = requests.get(SPOONACULAR_API_URL, params=params)
            response.raise_for_status()


            data = response.json()
            if 'results' in data:
                print("Recipes found:")
                for recipe in data['results']:
                    print(recipe)
            else:
                print("No recipes found")

            return response.json()


        except requests.exceptions.RequestException as e:

            return jsonify({'error': str(e)}), 500


@app.route("/result",methods=["GET","POST"])
@login_required
def result():
    if request.method=="POST":
        try:
            data = get_recipes()
            ids = [item['id'] for item in data['results']]
            SPOONACULAR_API_URL ="https://api.spoonacular.com/recipes/{id}/information"
            params = {
                'apiKey': API_KEY,
                'id': ids
            }
            recipes_info = []
            extended_ingredients={}
            for recipe_id in ids:
                response = requests.get(SPOONACULAR_API_URL.format(id=recipe_id), params=params)
                response.raise_for_status()
                ingredient_data = response.json()

                recipes_info.append(
                         ingredient_data )
                extended_ingredients.update({recipe_id:
                                            [ingredient["original"] for ingredient in ingredient_data["extendedIngredients"]]})

            return render_template("result.html",recipe = recipes_info,items=extended_ingredients)

        except requests.exceptions.RequestException as e:
            return jsonify({'error': str(e)}), 500

@app.route("/password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method=="GET":
        user= db.execute("SELECT username from users WHERE id = ?",session["user_id"])
        return render_template("pchange.html",user=user)

    if request.method=="POST":
        user= db.execute("SELECT username from users WHERE id = ?",session["user_id"])
        username = request.form.get("username")
        password = request.form.get("password")
        checks=0
        if not password or len(password)<6 or not password.isalnum():
            flash("Password must contain minimum 6 characters")
            return render_template("pchange.html",user=user)
        if request.form.get("password")==request.form.get("confirmation"):
            checks+=1
        else:
            flash("Please Enter your password correctly")
            return render_template("pchange.html",user=user)
        if checks==1:
            password_hash = generate_password_hash(password, method='pbkdf2', salt_length=16)
            db.execute("UPDATE users SET password=? WHERE username=?",password_hash,username)
        flash("Password Changed successfully")
        return redirect("/")


@app.route("/saverecipe", methods=["POST"])
@login_required
def save_recipe():
    data = request.get_json()
    print(data)
    recipe_id = data['id']
    recipe_title = data['title']
    print(recipe_id)
    print(session["user_id"])
    try:
        db.execute(
                "INSERT INTO recipes (user_id, title, recipe_id) VALUES (?, ?, ?)",
                session["user_id"], recipe_title, recipe_id
            )
        flash("Recipe saved")
        return jsonify({"status": "success", "message": "Recipe saved successfully!"}), 200
    except:
        flash("Recipe already Saved!!")
        return jsonify({"status": "error", "message": "Recipe already saved or an error occurred."}), 400


@app.route("/savedrecipes",methods=["GET","POST"])
@login_required
def savedrecipes():
    if request.method =="GET":
        try:
            id = db.execute("SELECT recipe_id from recipes WHERE user_id = ?",session["user_id"])
            title = db.execute("SELECT title from recipes WHERE user_id = ?",session["user_id"])
            ids = [i['recipe_id'] for i in id]
        except:
            return render_template("savedrecipes.html")
        print(ids)
        try:
            SPOONACULAR_API_URL ="https://api.spoonacular.com/recipes/{id}/information"
            params = {
                            'apiKey': API_KEY,
                            'id': ids
                        }
            recipes_info = []
            extended_ingredients={}
            for recipe_id in ids:
                response = requests.get(SPOONACULAR_API_URL.format(id=recipe_id), params=params)
                response.raise_for_status()
                ingredient_data = response.json()

                recipes_info.append(ingredient_data )
                extended_ingredients.update({recipe_id: [ingredient["original"] for ingredient in ingredient_data["extendedIngredients"]]})
            return render_template("savedrecipes.html",recipe = recipes_info,items=extended_ingredients)

        except requests.exceptions.RequestException as e:
            return jsonify({'error': str(e)}), 500


@app.route("/deleterecipe", methods=["POST"])
@login_required
def delete_recipe():
    data = request.get_json()
    recipe_id = data['id']
    recipe_title = data['title']

    if recipe_id and recipe_title:
        try:
            db.execute("DELETE FROM recipes  WHERE recipe_id = ? and user_id = ?",recipe_id,session["user_id"])
        except:
            flash("Recipe is already deleted!!")
    flash("Recipe deleted")
    return redirect("/")

