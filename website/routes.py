import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from website import app, db, bcrypt, socketio
from website.forms import RegistrationForm, LoginForm, EditAccountForm, UserSearchForm
from website.models import User, PublicMessage
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import send, emit


@socketio.on('message')
def handleMessage(msg):

    pub_msg = PublicMessage(sender_id = current_user.id, text = msg)
    db.session.add(pub_msg)
    db.session.commit()
    msg = '<p><b><a class="title mr-4" href={{ url_for("account_user", username =' + current_user.username + ') }}>' + current_user.username + ': </a></b>' + msg + '</p>'
    emit('message', msg, broadcast=True)


@app.route("/")
@app.route("/home")
def home():

    if current_user:
        return redirect(url_for('account'))
    else:
        return redirect(url_for('login'))


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/games")
def games():
    return render_template('games.html', title='About')


@app.route("/registration", methods=['GET', 'POST'])
def registration():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, country=form.country.data, city=form.city.data, text=form.text.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('registration.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():

    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, user = current_user)


def save_picture(form_picture_data):

    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture_data.filename)
    picture_filename = random_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)
    form_picture_data.save(picture_path)

    return picture_filename


@app.route("/account/edit", methods=['GET', 'POST'])
@login_required
def account_edit():

    form = EditAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.country = form.country.data
        current_user.city = form.city.data
        current_user.text = form.text.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.country.data = current_user.country
        form.city.data = current_user.city
        form.text.data = current_user.text
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('account_edit.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():

    form = UserSearchForm()
    users = User.query.filter_by()
    if form.validate_on_submit():
        if form.username.data:
            users = users.filter_by(username = form.username.data)
        if form.country.data:
            users = users.filter_by(country = form.country.data)
        if form.city.data:
            users = users.filter_by(city = form.city.data)
    users = users.all()

    return render_template('search.html', title='Account', form=form, users=users)


@app.route("/<string:username>", methods=['GET', 'POST'])
@login_required
def account_user(username):

    user = User.query.filter_by(username = username).first()
    image_file = url_for('static', filename='profile_pics/' + user.image_file)

    return render_template('account.html', title=user.username, user=user, image_file=image_file)


@app.route("/chat", methods=['GET', 'POST'])
@login_required
def chat():

    msg_list = PublicMessage.query.all()
    return render_template('chat.html', title='Chat', msg_list=msg_list)


