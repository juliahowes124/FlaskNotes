from flask import Flask, render_template, redirect, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Note

from forms import RegisterForm, LoginForm, NewNoteForm, UpdateNoteForm

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


#####Login Authentication####

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.username.data in session:
        return redirect(f'/users/{form.username.data}')

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
        return redirect(f'/users/{user.username}')

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
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Invalid username/password"]

    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    """ clear info from the session and redirect """

    session.pop("username", None)  # None
    flash('You were logged out')

    return redirect('/')

### User authorization ###


@app.route('/users/<username>')
def secret(username):

    if username != session["username"]:
        flash('You must be logged in to view')
        return redirect('/')
    else:
        user = User.query.get_or_404(username)
        return render_template('secret.html', user=user)


@app.route('/users/<username>/delete', methods=['POST'])  # why not delete?
def delete_user(username):
    """ remove user from db and also delete their notes
        redirect to root """

    user = User.query.get_or_404(username)

    if user.username != session.get("username"):
        flash("You aren't authorized to delete this user")
        return redirect('/login')
    else:
        db.session.delete(user)
        db.session.commit()
        session.pop("username", None)
        return redirect('/')

@app.route('/users/<username>/notes/add', methods=["GET", "POST"])
def add_note(username):
    form = NewNoteForm()

#"middleware"
    if username != session.get("username"):
        flash('Not authorized')
        return redirect('/')
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        note = Note(owner=username, title=title, content=content)
        db.session.add(note)
        db.session.commit()
        return redirect(f"/users/{username}")
    
    return render_template('create_note.html', form=form)

@app.route('/notes/<int:note_id>/update', methods=["GET", "POST"])
def update_note(note_id):

    note = Note.query.get_or_404(note_id)
    form = UpdateNoteForm(obj=note)

    if note.owner != session.get("username"):
        flash('Not authorized')
        return redirect('/')
    
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        return redirect(f"/users/{note.owner}")
    
    return render_template('update_note.html', form=form)


@app.route('/notes/<int:note_id>/delete', methods=["POST"])
def delete_note(note_id):

    note = Note.query.get_or_404(note_id)
    username = note.owner
    if username != session.get("username"):
        flash('Not authorized')
        return redirect('/')
    
    db.session.delete(note)
    db.session.commit()
    return redirect(f"/users/{username}")

