from flask import Flask
from sqlalchemy_utils.functions import database_exists, create_database

from controllers.userController import UserController
from models.database import db

# from routes.user_bp import UserBlueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost:3306/ir_pj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    create_database(app.config["SQLALCHEMY_DATABASE_URI"])

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/login', methods=['POST'])
def TEST():
    return UserController.login()


if __name__ == '__main__':
    app.run(debug=True)
