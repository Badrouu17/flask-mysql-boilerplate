# pylint: disable=E0602
import os


def init_mysql():
    from flask import current_app as app
    from flask_mysqldb import MySQL

    app.config['MYSQL_HOST'] = os.getenv(
        'MYSQL_HOST')
    app.config['MYSQL_PORT'] = int(
        os.getenv('MYSQL_PORT'))
    app.config['MYSQL_USER'] = os.getenv(
        'MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv(
        'MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv(
        'MYSQL_DB')
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    mysql = MySQL(app)

    return mysql


def use_db():
    if db:
        cnx = db.connection
        return cnx
    return False
