from flask import request, jsonify
from spellchecker import SpellChecker
import pickle
import pandas as pd

spell = SpellChecker(language='en')
title = pickle.load(open('E:/Compo-work/ir_pj_backend/assets/title.pkl', 'rb'))
parsed_data = pickle.load(open('E:/Compo-work/ir_pj_backend/assets/parsed_data5.pkl', 'rb'))
synopsis = pickle.load(open('E:/Compo-work/ir_pj_backend/assets/synopsis.pkl', 'rb'))


class AnimeSearch:
    @staticmethod
    def search_title():
        query = request.get_json()['input']
        spell_corr = [spell.correction(w) for w in query.split()]
        query = spell_corr[0]
        score = title.transform(query)
        df_bm = pd.DataFrame(data=parsed_data)
        df_bm['bm25'] = list(score)
        df_bm['rank'] = df_bm['bm25'].rank(ascending=False)
        df_bm = df_bm.nlargest(columns='bm25', n=12)
        df_bm = df_bm.drop(columns='bm25', axis=1)
        return jsonify({'query': query, 'spell_corr': spell_corr, 'info': df_bm.to_dict('records')}), 200

    @staticmethod
    def search_description():
        query = request.get_json()['input']
        spell_corr = [spell.correction(w) for w in query.split()]
        spell_corr = list(filter(None, spell_corr))
        spell_corr = " ".join(spell_corr)
        score = synopsis.transform(spell_corr)
        df_bm = pd.DataFrame(data=parsed_data)
        df_bm['bm25'] = list(score)
        df_bm['rank'] = df_bm['bm25'].rank(ascending=False)
        df_bm = df_bm.nlargest(columns='bm25', n=12)
        df_bm = df_bm.drop(columns='bm25', axis=1)
        return jsonify({'query': query, 'spell_corr': spell_corr, 'info': df_bm.to_dict('records')}), 200
