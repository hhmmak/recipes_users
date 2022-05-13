from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:

    db_name = 'recipes_schema'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made'].strftime("%Y-%m-%d") #convert datetime object to string of date only
        self.under_thirty_mins = data['under_thirty_mins']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

    #.. get methods

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db_name).query_db(query)
        recipes = []
        for row in results:
            recipes.append(cls(row))
        return recipes
    
    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id_num)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])

    #.. add methods
    @classmethod
    def add_one_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_thirty_mins, user_id, created_at, updated_at) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_thirty_mins)s, %(user_id)s,  NOW(), NOW());"
        return connectToMySQL(cls.db_name).query_db(query, data)



    #.. update methods
    @classmethod
    def change_one_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_thirty_mins = %(under_thirty_mins)s, updated_at = NOW() WHERE id = %(id_num)s;"
        connectToMySQL(cls.db_name).query_db(query, data)
        return cls

    #.. delete methods
    @classmethod
    def delete_one_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id_num)s;"
        connectToMySQL(cls.db_name).query_db(query, data)
        return cls


    #.. validation methods

