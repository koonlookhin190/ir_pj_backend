import pickle
import unittest
import bcrypt
import pandas as pd

from spellchecker import SpellChecker

title = pickle.load(open('E:/Compo-work/ir_pj_backend/assets/title.pkl', 'rb'))
parsed_data = pickle.load(open('E:/Compo-work/ir_pj_backend/assets/parsed_data5.pkl', 'rb'))


def spell_correction(query):
    spell = SpellChecker(language='en')
    query = query
    spell_corr = [spell.correction(w) for w in query.split()]
    return spell_corr[0]


def search_title(query):
    spell = SpellChecker(language='en')
    query = query
    spell_corr = [spell.correction(w) for w in query.split()]
    query = spell_corr[0]
    score = title.transform(query)
    df_bm = pd.DataFrame(data=parsed_data)
    df_bm['bm25'] = list(score)
    df_bm['rank'] = df_bm['bm25'].rank(ascending=False)
    df_bm = df_bm.nlargest(columns='bm25', n=12)
    df_bm = df_bm.drop(columns='bm25', axis=1)
    return df_bm['title'].iloc[0]


class TestCase(unittest.TestCase):
    def test_spell_correction(self):
        actual = spell_correction('naruta')
        expected = 'naruto'
        self.assertEqual(actual, expected)

    def test_seach_title(self):
        actual = search_title('naruto')
        expected = 'naruto'
        self.assertEqual(actual, expected)