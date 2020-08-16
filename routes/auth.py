from flask import render_template, redirect, url_for, session
from flask_login import current_user, login_user, logout_user

from forms import LoginForm
from model import DBUser


def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.main'))
    session['name'] = ""
    form = LoginForm()
    if form.validate_on_submit():
        if not DBUser.check_user(form.username.data, form.password.data):
            return redirect(url_for('routes.login'))
        login_user(DBUser.get_user(name=form.username.data))
        return redirect(url_for('routes.main'))
    return render_template('login.html', form=form)


def logout():
    logout_user()
    session['name'] = ""
    return redirect(url_for('routes.login'))

