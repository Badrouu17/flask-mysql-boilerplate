from flask import Blueprint
from controllers import authController

user = Blueprint(
    'user', __name__)


user.add_url_rule('/signup', 'signup', authController.signup,
                  methods=['POST'])

user.add_url_rule('/login', 'login', authController.login,
                  methods=['POST'])

user.add_url_rule('/forgotPassword', 'forgotPassword', authController.forgotPassword,
                  methods=['POST'])

user.add_url_rule('/resetPassword/<token>', 'resetPassword', authController.resetPassword,
                  methods=['PATCH'])
