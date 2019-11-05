from flask import Flask
from reviews import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///unbiased.db'

db = SQLAlchemy(app)

class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable = False)
    password = db.Column(db.String(50), nullable = False)
    role = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return 'userId = {0}, username = {1}, password = {2}, role = {3}'.format(self.userId, self.username, self.password, self.role)

class Genre(db.Model):
    genreId = db.Column(db.String(100), primary_key=True)
    description = db.Column(db.String(50), nullable = True)

    def __repr__(self):
        return 'genreId = {0}, description = {1}'.format(self.genreId,self.description)

class Game(db.Model):
    gameId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    rating = db.Column(db.Float, nullable = True)
    description = db.Column(db.String(20000), nullable = True)
    credibility = db.Column(db.Float, nullable = True)
    reviewAI = db.Column(db.String(10000), nullable = True)

    def __repr__(self):
        return 'gameId = {0}, title = {1}, rating = {2}, description = {3}, credibility = {4}, reviewAI = {5}'.format(self.gameId, self.title,self.rating,self.description,self.credibility,self.reviewAI)

GenreGame = db.Table('GenreGame',
    db.Column('genreId', db.String(100), db.ForeignKey('genre.genreId'), primary_key=True),
    db.Column('gameId', db.Integer, db.ForeignKey('game.gameId'), primary_key=True)
)

class Comment(db.Model):
    commentId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable = False)
    gameId = db.Column(db.Integer, db.ForeignKey('game.gameId'), nullable = False)
    content = db.Column(db.String(10000), nullable = False)
    creationDateTime = db.Column(db.DateTime, nullable = False, default=datetime.now())

    def __repr__(self):
        return 'commentId = {0}, userId = {1}, gameId = {2}, content = {3}, creationDateTime = {4}'.format(self.commentId, self.userId, self.gameId, self.content, self.creationDateTime)
        