from mysql.mysql import use_db
from flask import request as req, abort
from utils.response import res
from sql.userQueries import deleteUser, updatUserPhoto, updateUserEmail, updateUserName, getUserWithId
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url


def uploadToCloud():
    file_to_upload = req.files['file']
    if file_to_upload:
        upload_result = upload(
            file_to_upload)
        photo_url = cloudinary_url(upload_result['public_id'],
                                   format="jpg",
                                   crop="fill",
                                   width=500,
                                   height=500)
        return photo_url

    return abort(400, 'photo couldnt upload, try later')


def savePhotoInDb(url):
    if url:
        req.user["photo"] = url[0]
        cnx = use_db()
        db = cnx.cursor()
        db.execute(updatUserPhoto(
            req.user["user_id"], url[0]))
        cnx.commit()
        return url
    return abort(400, 'photo couldnt be saved in the db')


def uploadPhotos():
    url = uploadToCloud()
    savePhotoInDb(url)
    return res(200, {"msg": "photo uploeded successfully!"})


def updateMe():

    data = req.get_json()
    if "password" in data:
        abort(
            400, 'please use updatePassowrd endpoint to update the password.')

    cnx = use_db()
    db = cnx.cursor()

    if "email" in data:
        db.execute(updateUserEmail(
            req.user["user_id"], data["email"]))
        cnx.commit()
    if "name" in data:
        db.execute(updateUserName(
            req.user["user_id"], data["name"]))
        cnx.commit()
    db.execute(getUserWithId(
        req.user["user_id"]))
    user = db.fetchone()
    req.user = user
    return res(200, user)


def getMe():
    return res(200, {"user": req.user})


def deleteMe():
    cnx = use_db()
    db = cnx.cursor()
    db.execute(deleteUser(
        req.user["user_id"]))
    cnx.commit()
    return res(200, {
        "msg": "deleted successfully!"})
