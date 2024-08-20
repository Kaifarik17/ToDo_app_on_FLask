from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

import sqlalchemy as sa

from todo_app import db
from todo_app.auth.forms import LoginForm, RegisterForm
from todo_app.auth import auth_bp
from todo_app.models import User


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered!')

        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data)
        )
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            return redirect(url_for('main.index'))
        flash('Invalid email or password')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout/')
def logout():
    logout_user()
    
    return redirect(url_for('main.index'))