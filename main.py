import pandas as pd
from flask import Flask, request, jsonify
from sqlalchemy_utils.functions import database_exists, create_database
from controllers.userController import UserController
from models import Bookmark
from models.database import db
from flask_cors import CORS
from controllers.animeController import AnimeSearch
from controllers.suggestionController import top_list
import pickle

parsed_data = pickle.load(open('E:/Compo-work/ir_pj_backend/assets/parsed_data5.pkl', 'rb'))

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
    print(save_bm)
    db.session.delete(save_bm)
    db.session.commit()
    return jsonify('Delete'), 200


@app.route('/getBookmark', methods=['POST'])
def get_bookmark():
    user_id = request.get_json()['user_id']
    save_bookmark = db.session.query(Bookmark).filter_by(user_id=user_id).all()
    save_bookmark = Bookmark.read_list(save_bookmark)
    animes_bookmark = []
    for i in save_bookmark:
        temp = parsed_data[parsed_data['mal_id'] == i['anime_id']].to_dict('records')[0]
        animes_bookmark.append(
            {'mal_id': temp['mal_id'], 'title': temp['title'], 'images': temp['images'], 'score': i['score']})

    animes_bookmark.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({'animes_bookmark': animes_bookmark}), 200


# @app.route('/getSuggestion', methods=['POST'])
# def suggestion():
#     user_id = request.get_json()['user_id']
#     save_bookmark = db.session.query(Bookmark).filter_by(user_id=user_id).all()
#     save_bookmark = Bookmark.read_list(save_bookmark)
#     keep_genere = ["Action",
#                    "Drama",
#                    "Action",
#                    "Fantasy",
#                    "Action",
#                    "Adventure",
#                    "Fantasy",
#                    "Action",
#                    "Adventure",
#                    "Fantasy",
#                    "Action"]
#     genre_names = [
#         'Action', 'Adventure', 'Comedy', 'Drama', 'Sci-Fi',
#         'Game', 'Space', 'Music', 'Mystery', 'School', 'Fantasy',
#         'Horror', 'Kids', 'Sports', 'Magic', 'Romance',
#     ]
#     score = [
#         0, 0, 0, 0, 0,
#         0, 0, 0, 0, 0, 0,
#         0, 0, 0, 0, 0,
#     ]
#     df = pd.DataFrame({'category': genre_names, 'score': score})
#
#     for i in save_bookmark:
#         temp = parsed_data[parsed_data['mal_id'] == i['anime_id']].to_dict('records')[0]
#         for j in temp['genres']:
#             keep_genere.append(j)
#
#     res = []
#     for a in genre_names:
#         # print(a)
#         for k in keep_genere:
#             if k == a:
#                 res.append(k)
#
#     print(res)
#
#     for a in range(len(genre_names)):
#         for k in df['category']:
#             keep = 1
#             for l in res:
#                 if k == l:
#                     df['score'].values[a] = keep
#                     keep = keep+1

#
# return jsonify({'keep_genere': keep_genere}), 200


# @app.route('/getSuggestion', methods=['POST'])
# def suggestion():
#     user_id = request.get_json()['user_id']
#     save_bookmark = db.session.query(Bookmark).filter_by(user_id=user_id).all()
#     save_bookmark = Bookmark.read_list(save_bookmark)
#     df_book = pd.DataFrame(save_bookmark)
#     print(df_book)
#     df_book = df_book.drop(columns='id', axis=1)
#     user_df = pd.DataFrame(df_book)
#     print(user_df)
#     user_df = make_user_feature(user_df)
#     print(user_df)
#     return jsonify({suggestion_u(user_df, 10, parsed_data, df_book)}),200
#     # user_df = make_user_feature(user_df)

@app.route('/get_topList', methods=['GET'])
def top_12():
    return top_list()


if __name__ == '__main__':
    app.run(debug=True)
