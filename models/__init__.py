import bcrypt
from sqlalchemy import event
from .user import User
from .database import db


@event.listens_for(User.__table__ , 'after_create')
def create_user(*args, **kwargs):
    db.session.add(
        User(username='koonlookhin', password=bcrypt.hashpw('1234567'.encode('utf-8'), bcrypt.gensalt(10)),
             firstname='krit', lastname='tipnuan', email='lookhinganthe@hotmail.com'))
    db.session.commit()
