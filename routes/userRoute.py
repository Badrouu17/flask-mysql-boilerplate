from flask import Blueprint
from controllers import userController

user = Blueprint('user', __name__)


user.add_url_rule('/login', 'login', userController.login,
                  methods=['GET', 'POST'])
