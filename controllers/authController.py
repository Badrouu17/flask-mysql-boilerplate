from mysql.mysql import use_db
from flask import request as req, abort
from utils.response import res
from utils.password import (hashPassword, comparePasswords,
                            changedPasswordAfter,
                            createPasswordResetToken, cryptToken)
from utils.jwt import (
    signToken, checkToken)

from sql.userQueries import (
    insertUser, getUserWithId,
    getUserWithEmail, getUserByResetToken,
    updateUserEmail, updateUserName,
    updateUserPassResetData, updatUserPhoto, updateResetPassword)

from utils.mail import Mailer
import time


def createSendToken(user):
    token = signToken(
        user["user_id"])
    # remove password from output
    del user["password"]
    return res(200, {"token": token, "user": user})

# authentication


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


def forgotPassword():
    # 1) Get user based on POSTed email
    data = req.get_json()
    if "email" not in data:
        return abort(400, 'please provide an email')

    cnx = use_db()
    db = cnx.cursor()
    db.execute(getUserWithEmail(
        data["email"]))
    result = db.fetchall()
    if result == ():
        abort(
            400, 'no user with this email')

    user = result[0]
    # 2) Generate the random reset token
    tokenData = createPasswordResetToken()
    # 3) save token reset data in db
    db.execute(updateUserPassResetData(
        user["user_id"], tokenData["prt"], tokenData["pre"]))
    cnx.commit()
    # 4) Send it to user's email
    try:
        rt = tokenData["rt"]
        resetURL = f"https://127.0.0.1:3001/resetPassword/{rt}"
        print(resetURL)
        Mailer(username="",
               password="",
               server="smtp.gmail.com",
               port=587).sendText(subject="resetPassword",
                                  source="",
                                  to="",
                                  content=resetURL)

        res(200, {
            "msg": "mail send successfully"})
    except:
        # db.execute(updateUserPassResetData(
        #     user["user_id"], "NULL", "NULL"))
        # cnx.commit()
        abort(
            400, 'an error during sending the email, please try again')


def resetPassword(token):
    # 1) Get user based on the token
    cryptedToken = cryptToken(
        token)
    cnx = use_db()
    db = cnx.cursor()
    now = int(
        round(time.time() * 1000))
    db.execute(getUserByResetToken(
        cryptedToken, now))
    user = db.fetchone()
    # 2) If token has not expired, and there is user, set the new password
    if "user_id" not in user:
        abort(
            400, "Token is invalid or has expired")
    # 3) hash an Update password, changedPasswordAt property for the user
    data = req.get_json()
    if ("password" not in data):
        return abort(
            400, 'please provide an password')

    hashed = hashPassword(
        data["password"])

    nowDate = int(
        round(time.time() * 1000))
    db.execute(updateResetPassword(
        user["user_id"], hashed, nowDate))
    cnx.commit()
    # 4) Log the user in, send JWT
    return createSendToken(user)


def updatePassword():
    data = req.get_json()
    if "currentPassword" not in data or "newPassword" not in data:
        abort(
            400, "please enter the needed data!")

    cnx = use_db()
    db = cnx.cursor()
    db.execute(getUserWithId(
        req.user["user_id"]))
    user = db.fetchone()

    if "name" not in user:
        abort(
            400, "cant find this user")

    if not comparePasswords(user["password"], data["currentPassword"]):
        abort(
            401, 'Your current password is wrong')

    hashed = hashPassword(
        data["newPassword"])
    nowDate = int(
        round(time.time() * 1000))

    db.execute(updateResetPassword(
        req.user["user_id"], hashed, nowDate))
    cnx.commit()

    db.execute(getUserWithId(
        req.user["user_id"]))
    user = db.fetchone()

    # send the token
    return createSendToken(user)


def protect():
    # 1) Getting token and check of it's there
    if "Authorization" not in req.headers:
        abort(
            401, 'you are not logged in, please login')

    token = req.headers["Authorization"].split(' ')[
        1]

    # 2) Verification token
    try:
        decoded = checkToken(
            token)
    except:
        abort(
            401, 'wrong or expired token.')

    # 3) Check if user still exists
    cnx = use_db()
    db = cnx.cursor()
    db.execute(
        getUserWithId(decoded["id"]))
    user = db.fetchone()
    if "user_id" not in user:
        abort(
            401, 'The user belonging to this token does no longer exist.')

    # 4) Check if user changed password after the token was issued
    if changedPasswordAfter(decoded["iat"], user["password_changed_at"]):
        return abort(401, 'User recently changed password! Please log in again.')

    # GRANT ACCESS TO PROTECTED ROUTE
    del user["password"]
    req.user = user
