#!/usr/bin/python2
# coding: utf-8

import re
import urllib2

from lxml.html.clean import Cleaner
from flask import Flask, request, render_template, flash, redirect, url_for
from flask.ext.login import LoginManager, current_user, login_required, \
    login_user, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "guess-the-secret-key"

cleaner = Cleaner()
cleaner.javascript = True
cleaner.style = True

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, name, password, active=True):
        self.id = id
        self.name = name
        self.set_password(password)
        self.active = active

    def is_active(self):
        return self.active

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


USERS = {
    1: User(1, u"John", u"guess-the-secret"),
}
USERNAMES = dict((u.name, u) for u in USERS.itervalues())


@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    remember_me = True if 'remember_me' in request.form else False
    if not username in USERNAMES:
        flash("Failed.")
        return redirect(url_for('login'))
    u = USERNAMES[username]

    if not u.check_password(password):
        flash("Failed.")
        return redirect(url_for('login'))
    login_user(USERNAMES[username], remember=remember_me)
    flash("Logged in.")
    return redirect(request.args.get("next") or url_for("index"))


@app.route('/logout')
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))


@app.route('/f')
@login_required
def fetch():
    url = request.args.get('url', '')
    if re.match(r'^https?://\w.+$', url):
        html = urllib2.urlopen(url).read()
        return cleaner.clean_html(html)
    return "Invalid URL."


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
