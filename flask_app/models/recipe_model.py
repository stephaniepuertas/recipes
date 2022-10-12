from flask_app import flash
from pprint import pprint
# must import user now so you can use it 
from flask_app.models.user_model import User

from flask_app.config.mysqlconnection import connectToMySQL

DATABASE = 'recipe_schema'


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30mins = data['under_30mins']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # must add for the foreign key
        self.user_id= data['user_id']
        # user obtained by user id(join)
        self.user=data['user']
    
    def __repr__(self):
        return f'<Recipe: {self.name}>'

    @staticmethod
    def validate_recipe(form):
        is_valid = True
        if len(form['name']) < 3:
            flash('Name must be at least three characters.', 'name')
            is_valid = False
        if len(form['description']) < 3:
            flash('description must be at least three characters.', 'description')
            is_valid = False
        if len(form['instructions']) < 3:
            flash('instructions must be at least three characters.', 'instructions')
            is_valid = False
    #make sure you add NOT for date form--->
        if not form['date_made']:
            flash('Date must not be blank.', 'date_made')
            is_valid = False
        return is_valid

    # create a recipe
    @classmethod
    def save(cls, data):
        # must add the hidden session id 
        query = 'INSERT INTO recipes (name, description, instructions, date_made, under_30mins, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30mins)s, %(user_id)s);'
        recipe_id = connectToMySQL(DATABASE).query_db(query, data)
        return recipe_id

    # find all recipes (no data needed)
    @classmethod
    def find_all(cls):
        query = 'SELECT * from recipes;'
        results = connectToMySQL(DATABASE).query_db(query)
        recipes = []
        for result in results:
            recipes.append(Recipe(result))
        return recipes

# necessary for join!!!!!!!
    # find all recipes with creator (no data needed)
    @classmethod
    def find_all_with_creator(cls):
        query = 'SELECT * from recipes;'
        results = connectToMySQL(DATABASE).query_db(query)
        pprint(results)
        recipes = []
        for result in results:
            data={
                'id': result['user_id']
            }
            user= User.find_by_id(data)
            recipe_data= {
                'id': result['id'],
                'name': result['name'],
                'description': result['description'],
                'instructions': result['instructions'],
                'date_made': result['date_made'],
                'under_30mins': result['under_30mins'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
                'user_id': result['user_id'],
                'user': user
            }
            recipes.append(Recipe(recipe_data))
        return recipes

    # find one recipe by id
    @classmethod
    def find_by_id(cls, data):
        query = 'SELECT * from recipes WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        recipe = Recipe(results[0])
        return recipe

    # find one recipe by id with creator
    @classmethod
    def find_by_id_with_creator(cls, data):
        query = 'SELECT * from recipes WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        data={
                'id': results[0]['user_id']
        }
        user= User.find_by_id(data)
        recipe_data= {
            'id': results[0]['id'],
            'name': results[0]['name'],
            'description': results[0]['description'],
            'instructions': results[0]['instructions'],
            'date_made': results[0]['date_made'],
            'under_30mins': results[0]['under_30mins'],
            'created_at': results[0]['created_at'],
            'updated_at': results[0]['updated_at'],
            'user_id': results[0]['user_id'],
            'user': user
        }
        recipe = Recipe(recipe_data)
        return recipe

    # update one recipe by id
    @classmethod
    def find_by_id_and_update(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30mins = %(under_30mins)s WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True

    # delete one recipe by id
    @classmethod
    def find_by_id_and_delete(cls, data):
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True