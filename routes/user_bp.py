from flask import Blueprint
from controllers.userController import UserController


class UserBlueprint:
    user_bp = Blueprint('user_bp', __name__, url_prefix='/user')
    user_bp.route('/login', methods=['POST'])(UserController.login())
