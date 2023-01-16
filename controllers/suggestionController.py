import pickle
from sklearn.model_selection import train_test_split
from flask_sqlalchemy import SQLAlchemy
import seaborn as sns
import numpy as np
import pandas as pd
import lightgbm as lgb
import matplotlib.pyplot as plt

from models import Bookmark

db = SQLAlchemy()

parsed_data = pickle.load(open('E:/Compo-work/ir_pj_backend/assets/parsed_data5.pkl', 'rb'))


# def suggestion():

#
# def make_user_feature(df):
#     # add user feature
#     df['score_count'] = df.groupby('user_id')['anime_id'].transform('count')
#     df['score'] = df.groupby('user_id')['score'].transform('mean')
#     return df

#
# def suggestion_u(user_df, top_k, anime, rating):
#     genre_names = [
#         'Action', 'Adventure', 'Comedy', 'Drama', 'Sci-Fi',
#         'Game', 'Space', 'Music', 'Mystery', 'School', 'Fantasy',
#         'Horror', 'Kids', 'Sports', 'Magic', 'Romance',
#     ]
#
#     merged_df = parsed_data.drop(['mal_id'], axis=1)
#
#     fit, blindtest = train_test_split(merged_df, test_size=0.2, random_state=0)
#     fit_train, fit_test = train_test_split(fit, test_size=0.3, random_state=0)
#
#     user_col = 'user_id'
#     target_col = 'score'
#
#     fit_train = fit_train.sort_values('score').reset_index(drop=True)
#     print(fit_train.head(10).to_markdown())
#     fit_test = fit_test.sort_values('score').reset_index(drop=True)
#     blindtest = blindtest.sort_values('score').reset_index(drop=True)
#
#     fit_train_query = fit_train[target_col].value_counts().sort_index()
#     print(fit_train_query.head(10).to_markdown())
#     fit_test_query = fit_test[target_col].value_counts().sort_index()
#
#     model = lgb.LGBMRanker(n_estimators=1000, random_state=0)
#     model.fit(
#         group=fit_train_query,
#         eval_set=[(fit_test[genre_names], fit_test[target_col])],
#         eval_group=[list(fit_test_query)],
#         eval_at=[1, 3, 5, 10],  # calc validation ndcg@1,3,5,10
#         early_stopping_rounds=100,
#         verbose=10
#     )
#
#
#
#     model.predict(blindtest.iloc[:10][genre_names])
#     plt.figure(figsize=(10, 7))
#     df_plt = pd.DataFrame({'feature_name': genre_names, 'feature_importance':
#         model.feature_importances_})
#     df_plt.sort_values('feature_importance', ascending=False, inplace=True)
#     sns.barplot(x="feature_importance", y="feature_name", data=df_plt)
#     plt.title('feature importance')
#
#     user_anime_df = anime.merge(rating, left_on='mal_id', right_on='anime_id')
#     user_anime_df = make_user_feature(user_anime_df)
#     excludes_genres = list(np.array(genre_names)[np.nonzero([user_anime_df[genre_names].sum(axis=0)
#                                                              <= 1])[1]])
#     pred_df = make_user_feature(anime.copy())
#     pred_df = pred_df.loc[pred_df[excludes_genres].sum(axis=1) == 0]
#
#     for col in user_df.columns:
#         if col in genre_names:
#             pred_df[col] = user_df[col].values[0]
#     preds = model.predict(pred_df[genre_names])
#     topk_idx = np.argsort(preds)[::-1][:top_k]
#     recommend_df = pred_df.iloc[topk_idx].reset_index(drop=True)
#
#     return recommend_df
#
#
# # user_id = 1
# # save_bookmark = db.session.query(Bookmark).filter_by(user_id=user_id).all()
# # save_bookmark = Bookmark.read_list(save_bookmark)
# # df_book = pd.DataFrame(save_bookmark)
# # print(df_book)
# # df_book = df_book.drop(columns='id', axis=1)
# # user_df = pd.DataFrame(df_book)
# # print(user_df)
# # user_df = make_user_feature(user_df)
# # print(user_df)
# # suggestion_u(user_df, 10, parsed_data, df_book)

