from mysql.mysql import use_db
from flask import request as req, abort
from utils.response import res
from utils.password import (hashPassword, comparePasswords,
                            changePasswordAfter,
                            createPasswordResetToken)
from utils.jwt import (
    signToken)

from sql.userQueries import (
    insertUser, getUserWithId,
    getUserWithEmail, getUserByResetToken,
    updateUserEmail, updateUserName,
    updateUserPassResetData, updatUserPhoto)


def createSendToken(user):
    token = signToken(
        user["user_id"])
    # remove password from output
    del user["password"]
    return res(200, {"token": token, "user": user})


def signup():
    data = req.get_json()

    newUser = {
        "name": data["name"],
        "email": data["email"],
        "password": hashPassword(data["password"])
    }
    cnx = use_db()
    db = cnx.cursor()
    # insert the new user
    db.execute(
        insertUser(newUser))
    cnx.commit()
    # get the same new user
    db.execute(getUserWithEmail(
        newUser["email"]))
    resulat = db.fetchall()
    return createSendToken(resulat[0])


def login():
    # 1) Check if email and password exist
    data = req.get_json()
    if ("email" not in data or "password" not in data):
        return abort(
            400, 'please provide an email and password')

    # 2) Check if user exists
    cnx = use_db()
    db = cnx.cursor()
    db.execute(getUserWithEmail(
        data["email"]))
    result = db.fetchall()
    if result == ():
        return abort(
            400, 'no user with this email')

    user = result[0]

    # 3) check password is correct
    if not comparePasswords(user["password"], data["password"]):
        return abort(
            400, 'the password you enterd is wrong, please try again')

    # 4) If everything ok, send token to client
    return createSendToken(user)
