def insertUser(user):
    name, email, password = (
        user["name"], user["email"], user["password"])

    return f"""INSERT INTO users(name, email, password) 
               VALUES('{name}', '{email}', '{password}')"""


def getUserWithEmail(email):
    return f""" SELECT user_id,name,email,photo,password
                FROM users
                WHERE users.email = '{email}' """


def getUserWithId(id):
    return f""" SELECT user_id,name,email,photo,password,password_changed_at
                FROM users
                WHERE users.user_id = {id} """


def updateUserPassResetData(id, prt, pre):
    return f""" UPDATE users
                SET users.password_reset_token = '{prt}' ,users.password_reset_expires = {pre}
                WHERE users.user_id = {id} """


def getUserByResetToken(prt, now):
    return f""" SELECT user_id,name,email,photo,password
                FROM users
                WHERE users.password_reset_token = '{prt}'
                AND
                users.password_reset_expires > {now} """


def resetPassword(id, psw, pca):
    return f""" UPDATE users
                SET users.password = '{psw}', 
                users.password_reset_token = NULL, 
                users.password_reset_expires = NULL,
                users.password_changed_at = {pca}
                WHERE users.user_id = {id} """


def updateUserEmail(id, email):
    return f""" UPDATE users
                SET email = '{email}'
                WHERE users.user_id = {id} """


def updateUserName(id, name):
    return f""" UPDATE users
                SET name = '{name}'
                WHERE users.user_id = {id} """


def updatUserPhoto(id, photo):
    return f""" UPDATE users
                SET photo = '{photo}'
                WHERE users.user_id = {id} """


def deleteUser(id):
    return f""" DELETE FROM users
                WHERE users.user_id = {id} """
