from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models import user, recipe

bcrypt = Bcrypt(app)

#.. Visible Routes

@app.route('/')
def index():
    if "id" in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if "id" not in session:   # avoid access of user-sensitive routes without proper login
        print(f"--------- no session['id']")
        return redirect('/')
    data = {
        "id": session['id']
    }
    recipes_list = recipe.Recipe.get_all_recipes()
    return render_template('dashboard.html', user_name = session['user_name'], recipes = recipes_list)

#.. Invisible Routes

@app.route('/register', methods=['POST'])
def create_account_route():
    # create only if passed validation
    if user.User.validate_create_account(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            # "birthday": request.form['birthday'],
            "email": request.form['email'],
            "password": pw_hash
        }
        user.User.add_account(data)
        print("---------created user")
    return redirect ('/')

@app.route('/login', methods=['POST'])
def login_account():
    data = {
        "email": request.form['email'],
    }
    user_account = user.User.get_account_by_email(data)
    if not user_account or not bcrypt.check_password_hash(user_account.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['id'] = user_account.id
    session['user_name'] = user_account.first_name
    print(f"----------session['id'] = {session['id']}")
    return redirect('/dashboard')

@app.route('/logout')
def logout_account():
    session.clear()
    return redirect('/')
