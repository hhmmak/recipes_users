from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
# from datetime import timedelta, date

# TEN_YEARS_AGO = date.today() - timedelta(days=3650)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# PW_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)')

class User:


    db_name = 'recipes_schema'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #.. get methods
    
    @classmethod
    def get_account_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) <= 0: # return None if no match account found
            return False
        return cls(results[0])

    @classmethod
    def get_account_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) <= 0: # return None if no match account found
            return None
        return cls(results[0])
    
    #.. add methods

    @classmethod
    def add_account(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #.. validation methods

    @staticmethod
    def validate_create_account(data):
        is_valid = True
        # first name
        if len(data['first_name']) < 2:
            is_valid = False
            flash("Please enter a first name with more than 2 characters.")
        elif not data['first_name'].isalpha():
            is_valid = False
            flash("First name must contain only uppercase or lowercase letters.")
        # last name
        if len(data['last_name']) < 1:
            is_valid = False
            flash("Please enter a last name with more than 2 characters.")
        elif not data['last_name'].isalpha():
            is_valid = False
            flash("Last name must contain only uppercase or lowercase letters.")
        #birthday
        # print(f"----------birthday = {data['birthday']}, TEN_YEARS_AGO = {TEN_YEARS_AGO}")
        # if TEN_YEARS_AGO < date.fromisoformat(data['birthday']):
        #     is_valid = False
        #     flash("Account holder must be older than 10 years old.")
        #email
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("Please enter a valid email address.")
        #password
        # if not PW_REGEX.match(data['password']):
        #     is_valid = False
        #     flash("Password must include one Uppercase letter and one number.")
        if data['password'] != data['password_confirm']:
            is_valid = False
            flash("Passwords must match.")
        # check if account existed
        if is_valid and User.get_account_by_email(data):
            is_valid = False
            flash("Email address was previously registered. Please use another email address.")
        print(f"----------is_valid = {is_valid}")
        return is_valid