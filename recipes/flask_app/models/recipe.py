from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app, flash
from pprint import pprint
from datetime import date, datetime

DATABASE = 'recipes_schema'

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.under = data['under']
        self.description = data['description']
        self.instructions = data['instructions']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def select_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return Recipe(results[0]) 

    @classmethod
    def select_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(DATABASE).query_db(query)
        recipes = []
        for result in results:
            recipes.append( Recipe(result) )
        return recipes 

    @classmethod
    def insert_recipe(cls, data):
        query = "INSERT INTO recipes (name, under, description, instructions, user_id, created_at) VALUES (%(name)s, %(under)s, %(description)s, %(instructions)s, %(user_id)s, %(created_at)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under = %(under)s, created_at = %(created_at)s WHERE recipes.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE recipes.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return  

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True

        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters long.", 'name')
            is_valid = False

        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters long.", 'description')
            is_valid = False

        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters long.", 'instructions')
            is_valid = False

        if recipe['created_at'] == "":
            flash("Date required", 'created_at')
            is_valid = False
            return is_valid
        if (datetime.strptime(recipe['created_at'], '%Y-%m-%d').date()) > date.today():
            flash("Date invalid.", 'created_at')
            is_valid = False

        return is_valid
[]