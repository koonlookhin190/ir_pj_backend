from flask_sqlalchemy import SQLAlchemy
import jwt
from flask import request, jsonify
import bcrypt
from models.user import User

db = SQLAlchemy()


class UserController:
    @staticmethod
    def login():
        try:
            username = request.get_json()['username'].lower()
            password = request.get_json()['password']
            if not username or not password:
                return jsonify({'message': 'username, and password cannot be null'}), 400
            try:
                user = User.query.filter_by(username=username).first()
                if password == user.password:
                    return jsonify({'message': 'you are login'}), 200
                raise
            except:
                return jsonify({'message': 'username or password is incorrect'}), 401
        except:
            return jsonify({'message': 'The request body required username and password'}), 400
