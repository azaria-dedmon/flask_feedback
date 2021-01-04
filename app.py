from flask import Flask, render_template, request, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from models import connect_db, db, User, FeedBack
from forms import RegisterUser, LoginUser, FeedBackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()

@app.route('/')
def return_register():
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username=username, password=password, email=email,
                    first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()

        session['username'] = user.username 
        return redirect('/secret')
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginUser()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username=username, password=password)
        session['username'] = user.username 
        if session['username'] == user.username:
            return redirect(f'/users/{username}')
    else:
        return render_template("login.html", form=form)


@app.route('/users/<username>')
def get_user(username):
    user = User.query.get_or_404(username)
    feedback = user.feedbacks
    if session['username'] == user.username:  
        return render_template("user_details.html", user=user, feedback=feedback)
    else:
        flash("Please login first!")
        return redirect('/login')


@app.route('/secret')
def secret_reveal():
    if session['username'] == user.username:
        return "You made it!"
    else:
        flash("Please login first!")
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect("/")

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):

    if session['username'] == user.username:  
        delete_user = User.query.filter_by(username=username).delete()
        db.session.commit()
        session.pop('username')
        return redirect('/')
    else:
        flash("Please login first!")
        return redirect('login')

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    user = User.query.get_or_404(username)
    form = FeedBackForm()
    if form.validate_on_submit() and session['username'] == user.username :
        session['username'] = user.username 
        title = form.title.data
        content = form.content.data
        feedback = FeedBack(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    else:
        return render_template('feedback_form.html', user=user, form=form)


@app.route('/feedback/<feedback_id>/update', methods=["GET", "POST"])
def edit_feedback(feedback_id):
    feedback = FeedBack.query.get_or_404(feedback_id)
    form = FeedBackForm(obj=feedback)
    username = feedback.user.username
    session['username'] = username 
    if form.validate_on_submit() and session['username'] == username:
        session['username'] = user.username 
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f'/users/{username}')
    else:
        return render_template('feedback_form.html', form=form, feedback=feedback)

@app.route('/feedback/<feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    feedback = FeedBack.query.get_or_404(feedback_id)
    username = feedback.username
    if session['username'] == username:
        delete_feedback = FeedBack.query.filter_by(id=feedback_id).delete()
        db.session.commit()
        return redirect(f'/users/{username}')
    else:
        return redirect('/login')




