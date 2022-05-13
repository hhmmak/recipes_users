from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models import recipe
from datetime import date

#.. Visible Route

@app.route('/recipes/create')
def recipe_new():
    if "id" not in session:   # avoid access of user-sensitive routes without proper login
        print(f"--------- no session['id']")
        return redirect('/')

    today_date = date.today().strftime("%Y-%m-%d") #set as default time for date made
    # print(f"----------today_date = {today_date}, {type(today_date)}")
    return render_template('add_recipe.html', today = today_date)

@app.route('/recipes/<int:id_num>')
def recipe_view(id_num):
    if "id" not in session:   # avoid access of user-sensitive routes without proper login
        print(f"--------- no session['id']")
        return redirect('/')
    
    data = {
        "id_num": id_num
    }
    result = recipe.Recipe.get_one_recipe(data)
    result.instructions = result.instructions.split('\n')   # split up lines in instruction
    return render_template('recipes.html', recipe = result, user_name = session['user_name'])

@app.route('/recipes/edit/<int:id_num>')
def recipe_edit(id_num):
    if "id" not in session:   # avoid access of user-sensitive routes without proper login
        print(f"--------- no session['id']")
        return redirect('/')
    
    data = {
        "id_num": id_num
    }
    result = recipe.Recipe.get_one_recipe(data)
    return render_template('edit_recipe.html', recipe = result)


#.. Invisible Route

@app.route('/recipes/new', methods=['POST'])
def recipe_create():
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "under_thirty_mins": request.form['under_thirty_mins'],
        "user_id": session['id'] #id in session = user being logged in = users.id = foreign key of recipes.user_id
    }
    recipe.Recipe.add_one_recipe(data)
    return redirect('/dashboard')

@app.route('/recipes/update', methods=['POST'])
def recipe_update():
    data = {
        "id_num": request.form['id_num'],
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "under_thirty_mins": request.form['under_thirty_mins'],
    }
    recipe.Recipe.change_one_recipe(data)
    return redirect('/dashboard')

@app.route('/recipes/delete', methods=['POST'])
def recipe_delete():
    data = {
        "id_num": request.form['id_num']
    }
    recipe.Recipe.delete_one_recipe(data)
    return redirect('/dashboard')