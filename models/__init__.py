import bcrypt
from sqlalchemy import event
from .user import User
from .bookmark import Bookmark
from .database import db


@event.listens_for(User.__table__, 'after_create')
def create_user(*args, **kwargs):
    db.session.add(
        User(username='koonlookhin', password=bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt(10)),
             email='lookhinganthe@hotmail.com', ))
    db.session.commit()


@event.listens_for(Bookmark.__table__, 'after_create')
def create_bookmark(*args, **kwargs):
    db.session.commit()
