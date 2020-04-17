from flask import Blueprint
from controllers import authController

auth = Blueprint('auth', __name__)


auth.add_url_rule('/signup', 'signup', authController.signup, methods=['POST'])

auth.add_url_rule('/login', 'login', authController.login, methods=['POST'])

auth.add_url_rule('/forgotPassword', 'forgotPassword',
                  authController.forgotPassword, methods=['POST'])

auth.add_url_rule('/resetPassword/<token>', 'resetPassword',
                  authController.resetPassword, methods=['PATCH'])
