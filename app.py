from flask import Flask, render_template, redirect, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User

from forms import RegisterForm, LoginForm

from random import choice

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///notes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.username.data in session:
        return redirect('/')

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User.register(username, pwd, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()
        session["username"] = user.username
        return redirect('/secret')
    
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        user = User.authenticate(username, pwd)
        if user:
            session["username"] = user.username
            return redirect('/secret')
        else:
            form.username.errors = ["Invalid username/password"]

    return render_template("login.html", form=form)

@app.route('/secret')
def secret():

    if "username" not in session:
        flash('You must be logged in to view')
        return redirect('/')
    else:
        return render_template('secret.html')
