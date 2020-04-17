from flask import Blueprint
from controllers import userController, authController

user = Blueprint(
    'user', __name__)

user.before_request(authController.protect)

user.add_url_rule('/uploadPhotos', 'uploadPhotos',
                  userController.uploadPhotos, methods=['POST'])

user.add_url_rule('/getMe', 'getMe', userController.getMe, methods=['GET'])

user.add_url_rule('/updateMe', 'updateMe',
                  userController.updateMe, methods=['PATCH'])

user.add_url_rule('/updatePassword', 'updatePassword',
                  authController.updatePassword, methods=['PATCH'])

user.add_url_rule('/deleteMe', 'deleteMe',
                  userController.deleteMe, methods=['DELETE'])
