# pylint: disable=E0602


def init_mysql():
    from flask import current_app as app
    from flask_mysqldb import MySQL

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_PORT'] = 3306
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'admin'
    app.config['MYSQL_DB'] = 'batn-db'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    mysql = MySQL(app)

    return mysql


def use_db():
    if db:
        cur = db.connection.cursor()
        return cur
    return False
