from nltk import PorterStemmer, word_tokenize
from nltk.corpus import stopwords


def preProcess(s):
    ps = PorterStemmer()
    s = word_tokenize(s)
    stopwords_set = set(stopwords.words())
    s = [w for w in s if w not in stopwords_set]
    s = [ps.stem(w) for w in s]
    s = ' '.join(s)
    return s
