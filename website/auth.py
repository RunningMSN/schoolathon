from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('pages.home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        fruit_password = request.form.get('fruit')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.fruit_password, fruit_password):
                login_user(user, remember=True)
                return redirect(url_for('pages.home'))
            else:
                flash('Incorrect fruit, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        fruit_password = request.form.get('fruit')
        team = request.form.get('team')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        else:
            new_user = User(email=email, name=name, team=team, fruit_password=generate_password_hash(
                fruit_password, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('pages.home'))

    return render_template("register.html", user=current_user)