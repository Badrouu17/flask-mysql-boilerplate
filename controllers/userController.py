from mysql.mysql import use_db
from flask import request as req, abort
from utils.response import res
from sql.userQueries import deleteUser


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


def updateMe():
    return 'ok'
