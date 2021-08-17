from validation_app.config.mysqlconnection import connectToMySQL
from validation_app import app
from flask_bcrypt import Bcrypt
from flask import flash
import re

bcrypt = Bcrypt(app)
DATABASE = "validation"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO user (first_name, last_name, email, password,created_at, updated_at ) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() );"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls, data):
        query = 'SELECT * FROM user;'
        print('Getting all users...')
        results = connectToMySQL(DATABASE).query_db(query)
        all_users = []
        for result in results:
            all_users.append(cls(result))
        return all_users

    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM user WHERE id = %(id)s'
        user = connectToMySQL(DATABASE).query_db(query, data)
        return cls(user[0])

    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM user WHERE email = %(email)s'
        email = connectToMySQL(DATABASE).query_db(query, data)
        if len(email) < 1:
            return False
        return cls(email[0])

    @staticmethod
    def validate_registration(data):
        is_valid = True
        if User.get_by_email(data):
            flash('Email is already in use', 'email')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Please enter a valid format for your email address', 'email')
            is_valid = False
        if not data['first_name'].isalpha() or len(data['first_name']) < 2:
            flash(
                'First name must include only letters and be at least 2 characters long.', 'first_name')
            is_valid = False
        if not data['last_name'].isalpha() or len(data['last_name']) < 2:
            flash(
                'Last name must include only letters and be at least 2 characters long.', 'last_name')
            is_valid = False
        if len(data["password"]) < 8:
            flash('Password must be at least 8 characters', 'password')
        if not data["password"] == data["confirm"]:
            flash('Passwords does not match', 'password')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True
        user = User.get_by_email(data)
        if not user:
            print('Email did not exist')
            flash('Invalid Email/Password.', 'error')
            is_valid = False
        elif not bcrypt.check_password_hash(user.password, data['password']):
            print('Password did not match')
            flash('Invalid Email or Password.', 'error')
            is_valid = False
        return is_valid
