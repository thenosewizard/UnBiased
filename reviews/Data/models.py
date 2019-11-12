from datetime import datetime
from reviews import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(50), nullable = False)
    role = db.Column(db.String(50), nullable = False)
    comments = db.relationship('Comment', backref = 'user', lazy = True)
    feedback = db.relationship('Feedback', backref = 'user', lazy = True)

    def __repr__(self):
        return 'userId = {0}, username = {1}, password = {2}, role = {3}'.format(self.id, self.username, self.password, self.role)

GenreGame = db.Table('GenreGame',
    db.Column('genreId', db.Integer, db.ForeignKey('genre.genreId'), primary_key = True),
    db.Column('gameId', db.Integer, db.ForeignKey('game.gameId'), primary_key = True)
)

class Genre(db.Model):
    genreId = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(50), nullable = True)

    def __repr__(self):
        return 'genreId = {0}, description = {1}'.format(self.genreId,self.description)

class Game(db.Model):
    gameId = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    rating = db.Column(db.Float, nullable = True)
    description = db.Column(db.String(20000), nullable = True)
    credibility = db.Column(db.Float, nullable = True)
    reviewAI = db.Column(db.String(10000), nullable = True)
    comments = db.relationship('Comment', backref = 'game', lazy = True)
    genre = db.relationship('Genre', secondary = GenreGame, lazy = 'subquery', backref = db.backref('game', lazy = True))

    def __repr__(self):
        return 'gameId = {0}, title = {1}, rating = {2}, description = {3}, credibility = {4}, reviewAI = {5}'.format(self.gameId, self.title,self.rating,self.description,self.credibility,self.reviewAI)

class Comment(db.Model):
    commentId = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    gameId = db.Column(db.Integer, db.ForeignKey('game.gameId'), nullable = False)
    content = db.Column(db.String(10000), nullable = False)
    creationDateTime = db.Column(db.DateTime, nullable = False, default = datetime.now())

    def __repr__(self):
        return 'commentId = {0}, userId = {1}, gameId = {2}, content = {3}, creationDateTime = {4}'.format(self.commentId, self.userId, self.gameId, self.content, self.creationDateTime)

class Feedback(db.Model):
    feedbackId = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    category = db.Column(db.String(50), nullable = False)
    content = db.Column(db.String(1000), nullable = False)

    def __repr__(self):
        return '{}, {}, {}, {}'.format(self.feedbackId, self.userId, self.category, self.content)

# db.create_all()

# db.session.add_all(
#     [
#         User(username = 'abi.charan', email = 'abi@charan.com', password = 'Abi123', role = 'User'),
#         User(username = 'MyNameJeff', email = 'myname@jeff.com', password = 'JeffJeffJeff', role = 'User'),
#         Genre(name = 'Adventure', description = 'Go on a Journey and Explore!'),
#         Genre(name = 'Action', description = 'Stunt, Explosions & Fights!'),
#         Game(title = 'Legend of Zelda, Breath of the Wild', rating = 5.0, description = 'Explore the world and Save it from Ganon\'s wrath', credibility = 5.0, reviewAI = 'PERFECT 10/10'),
#         Comment(userId = 1, gameId = 1, content = 'Love it'),
#         Comment(userId = 2, gameId = 1, content = '10/10'),
#         Feedback(userId = 1, category = 'Technical', content = 'website too slow')
#     ]
# )

# insert = GenreGame.insert().values(genreId = 1, gameId = 1)
# insert2 = GenreGame.insert().values(genreId = 2, gameId = 1)
# db.session.execute(insert)
# db.session.execute(insert2)

# db.session.commit()