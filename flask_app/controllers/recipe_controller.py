from pprint import pprint
from flask_app import app, render_template, redirect, request, session, flash
from flask_app.models.recipe_model import Recipe
# import the primary key 
from flask_app.models.user_model import User



# display all recipes
@app.get('/recipes')
def all_recipes():
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data={
        'id': session['user_id']
    }
    user= User.find_by_id(data)
    # you use the find all creator to get the information of the creator
    recipes = Recipe.find_all_with_creator()

    print(f'**** FOUND - ALL RECIPES: ****')
    pprint(recipes)
    return render_template('dashboard.html', recipes = recipes, user= user)

# display one recipe by id
@app.get('/recipes/<int:recipe_id>')
def one_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data = {
        'id': recipe_id
    }
    recipe = Recipe.find_by_id_with_creator(data)
    print(f'**** FOUND - RECIPE ID: {recipe.id} ****')
    return render_template('one_recipe.html', recipe = recipe)

# display form to create a recipe
@app.get('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    return render_template('new_recipe.html')

# process form and create a recipe/ validates
@app.post('/recipes')
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    Recipe.save(request.form)
    return redirect('/recipes')

# display form to edit a recipe by id with creator
@app.get('/recipes/<int:recipe_id>/edit')
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data = {
        'id': recipe_id
    }
    recipe = Recipe.find_by_id_with_creator(data)
    print(f'**** FOUND - RECIPE ID: {recipe.id} ****')
    return render_template('edit_recipe.html', recipe = recipe)

# process form and update a recipe by id
# include the validation
@app.post('/recipes/<int:recipe_id>/update')
def update_recipe(recipe_id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/{recipe_id}/edit')
    Recipe.find_by_id_and_update(request.form)
    return redirect(f'/recipes/{recipe_id}')

# delete one recipe by id
@app.get('/recipes/<int:recipe_id>/delete')
def delete_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data = {
        'id': recipe_id
    }
    Recipe.find_by_id_and_delete(data)
    print(f'**** DELETED - RECIPE ID: {recipe_id} ****')
    return redirect('/recipes')

