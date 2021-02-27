from flask import Blueprint
from __init__ import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return 'Login'


@auth.route('/logout')
def logout():
    return 'Logout'