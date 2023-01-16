import pandas as pd
import string
import pickle
import numpy as np

def clean_data(path):
    df = pd.read_json(path, orient='records')
    df.drop(columns=['approved', 'titles', 'title_english', 'title_japanese', 'title_synonyms', 'trailer', 'producers',
                     'licensors', 'themes', 'airing', 'duration', 'episodes', 'explicit_genres', 'broadcast', 'season',
                     'source', 'status', 'year'],
            inplace=True)
    df['images'] = df['images'].apply(lambda x: x['jpg']['image_url'])
    df['studios'] = df['studios'].apply(lambda x: [i['name'] for i in x])
    df['genres'] = df['genres'].apply(lambda x: [i['name'] for i in x])
    df['demographics'] = df['demographics'].apply(lambda x: [i['name'] for i in x])

    cleaned_title = df['title']
    cleaned_title = cleaned_title.apply(lambda x: x.lower())
    cleaned_title = cleaned_title.apply(lambda x: x.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    df['title'] = cleaned_title

    cleaned_synopsis = df['synopsis']
    cleaned_synopsis = cleaned_synopsis.apply(lambda x: x.lower() if x is not None else '')
    cleaned_synopsis = cleaned_synopsis.apply(
        lambda x: x.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    df['synopsis'] = cleaned_synopsis

    cleaned_background = df['background']
    cleaned_background = cleaned_background.apply(lambda x: x.lower() if x is not None else '')
    cleaned_background = cleaned_background.apply(
        lambda x: x.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    df['background'] = cleaned_background

    cleaned_score = df['score']
    cleaned_score = cleaned_score.replace(np.NaN, 0)
    df['score'] = cleaned_score

    cleaned_scored_by = df['scored_by']
    cleaned_scored_by = cleaned_scored_by.replace(np.NaN, 0)
    df['scored_by'] = cleaned_scored_by

    pickle.dump(df, open('E:/Compo-work/ir_pj_backend/assets/parsed_data5.pkl', 'wb'))
    return df


df = clean_data('E:/Compo-work/ir_pj_backend/assets/anime.json')
