from .database import db


class Bookmark(db.Model):
    __tablename__ = 'bookmark'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    anime_id = db.Column(db.Integer)
    score = db.Column(db.Integer)

    def __init__(self, user_id, anime_id, score):
        self.user_id = user_id
        self.anime_id = anime_id
        self.score = score

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'anime_id': self.anime_id,
            'score': self.score
        }
