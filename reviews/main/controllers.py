from flask import Blueprint, render_template, flash, redirect, url_for, request
main = Blueprint('main', __name__, template_folder= "templates")
from reviews.main.forms import RegistrationForm, LoginForm, CheckReviewForm, IndexForm
from reviews.Data.models import User, Game, Feedback, GenreGame, Comment, GameLink
from reviews import db, bcrypt
from flask_login import login_user, current_user, logout_user
# import joblib
# import string 
#!pip install spacy
#!python -m spacy download en
# import spacy
# from spacy.lang.en.stop_words import STOP_WORDS
#creating a list for punctuations
# punc = string.punctuation
#list of stop_words
# nlp = spacy.load('en')
# from spacy.lang.en import English

# stopWords = spacy.lang.en.stop_words.STOP_WORDS
# engToken = English()

@main.route('/', methods = ['GET', 'POST'])
def index():
    form = IndexForm()
    result = form.search(form.query.data)
    return render_template("index.html",title="Index",form=form,result=result)

@main.route('/test')
def test():
    users = User.query.all()
    return users


@main.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email = form.email.data,password=hashed_password,role = "Member")
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.email.data}!","success")
        return redirect(url_for('main.login'))   
    return render_template("register.html",title="register",form=form)

@main.route("/login", methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Welcome {user.username}!","success")
            return redirect(url_for("main.index"))
        else:
            flash("Incorrect email or password!","danger")
    return render_template("login.html",title="Login", form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@main.route("/browse")
def browse():
    page = request.args.get('page', 1, type=int)
    games = Game.query.paginate(page= page, per_page=5)
    links = GameLink.query.paginate(page=page, per_page=5)
    return render_template("browse.html", games=games, data = zip(games.items, links.items))

# @main.route("/checkreview", methods = ['GET','POST'])
# def checkreview():
#     form = CheckReviewForm()
#     isbiased = False
#     if form.is_submitted():
#         if form.validate():
#             def tokenizer(review):
#                 tokens = engToken(review)
                
#                 #lemmitation
#                 #Assigning the base forms of words. For example, 
#                 #the lemma of “was” is “be”, and the lemma of “rats” is “rat”.
#                 lemmi_tokens =[]
#                 for word in tokens:
#                     if word.lemma_ != "-PRON-":
#                         lemmi_tokens.append(word.lemma_.lower().strip())
#                     else:
#                         lemmi_tokens.append(word.lower_)        
#                 #removing the stop words
#                 #stop words such as a, the, is, we, they
#                 stop_words = [word for word in lemmi_tokens if not word in stopWords and word not in punc]
                        
                #return the processed list of tokens
            # return stop_words
            # review = form.content.data
            # loaded_pipe = joblib.load("reviews\\AI\\finalized_model.sav")
            # result = loaded_pipe.predict([review])
            # if result == 1:
            #     isbiased = False
            # else:
            #     isbiased = True
            # flash("Please wait while we process your review", "success")
            
#         else:
#             flash("Please enter a review", "danger")
#     return render_template("checkreview.html", form=form)
