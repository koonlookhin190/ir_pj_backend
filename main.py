from flask import Flask
from flask_cors import CORS
from sqlalchemy_utils.functions import database_exists, create_database
from models.database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost:3306/ir_pj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    create_database(app.config["SQLALCHEMY_DATABASE_URI"])

db.init_app(app)
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run()