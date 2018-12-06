from datetime import datetime
from website import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    country = db.Column(db.String(75), nullable=False)
    city = db.Column(db.String(85), nullable=False)
    text = db.Column(db.Text(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "User ({}, {}, {}, {}, {})".format(self.username, self.country, self.city, self.email, self.image_file)


class PublicMessage(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    sender = db.relationship('User', backref='sent_pub_messages', lazy=True)

    def __repr__(self):
        return "User ({}, {})".format(self.sender_id, self.text)



''' The following models are not used yet '''

class Message(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text(200), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'),
        nullable=False)
    sender = db.relationship('User', backref='sent_messages', lazy=True)

    def __repr__(self):
        return "User ({}, {})".format(self.sender_id, self.text)


chat_user = db.Table('tags',
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


class Chat(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User', secondary=chat_user, lazy='subquery',
        backref=db.backref('chats', lazy=True))
    messages = db.relationship('Message', backref='chat', lazy=True)

    def __repr__(self):
        return "User ({}, {})".format(self.sender_id, self.text)

