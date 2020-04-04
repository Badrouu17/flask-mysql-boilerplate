from flask import Blueprint
from controllers import userController

user = Blueprint('user', __name__)


@user.route('/')
def show():
    return "heyyy from user route"


@user.route('/login')
def show2():
    return userController.login()
