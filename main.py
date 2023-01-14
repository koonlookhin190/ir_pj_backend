from flask import Flask, request, jsonify
from sqlalchemy_utils.functions import database_exists, create_database
from controllers.userController import UserController
from models import Bookmark
from models.database import db
from flask_cors import CORS
from controllers.animeController import AnimeSearch

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@127.0.0.1:3306/ir_pj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    create_database(app.config["SQLALCHEMY_DATABASE_URI"])

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/login', methods=['POST'])
def UserLogin():
    return UserController.login()


@app.route('/search', methods=['POST'])
def search():
    return AnimeSearch.search_title()


@app.route('/search_description', methods=['POST'])
def search_description():
    return AnimeSearch.search_description()


@app.route('/add_bookmark', methods=['POST'])
def add_bookmark():
    user_id = request.get_json()['user_id']
    anime_id = request.get_json()['anime_id']
    score = request.get_json()['score']
    save_bm = Bookmark(user_id, anime_id, score)
    db.session.add(save_bm)
    db.session.commit()
    return jsonify('Pass'), 200


@app.route('/remove_bookmark', methods=['POST'])
def delete_bookmark():
    user_id = request.get_json()['user_id']
    anime_id = request.get_json()['anime_id']
    save_bm = db.session.query(Bookmark).filter_by(user_id=user_id, anime_id=anime_id).first()
    db.session.delete(save_bm)
    db.session.commit()
    return jsonify('Delete'), 200


if __name__ == '__main__':
    app.run(debug=True)
