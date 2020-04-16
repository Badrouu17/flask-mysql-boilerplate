from flask import Blueprint
from controllers import userController, authController

user = Blueprint(
    'user', __name__)

user.before_request(
    authController.protect)

user.add_url_rule('/getme', 'getme', userController.getMe,
                  methods=['GET'])

user.add_url_rule('/updatePassword', 'updatePassword', authController.updatePassword,
                  methods=['PATCH'])

user.add_url_rule('/deleteMe', 'deleteMe', userController.deleteMe,
                  methods=['DELETE'])
