import datetime
from xml.etree.ElementTree import \
    tostring

from Cryptodome import (
    Hash,
    Random)
from flask_bcrypt import (
    check_password_hash,
    generate_password_hash)


def hashPassword(password):
    return generate_password_hash(password, 12).decode('UTF-8')


def comparePasswords(curr, new):
    return check_password_hash(curr, new)


def parseDate(myDateTime):
    res = (datetime.datetime(myDateTime.year, myDateTime.month, myDateTime.day, myDateTime.hour,
                             myDateTime.minute, myDateTime.second) - datetime.datetime(1970, 1, 1)).total_seconds()
    return res


def changePasswordAfter(jwtTimestamp, passwordChangedAt):
    if passwordChangedAt:
        changedTime = parseDate(
            passwordChangedAt) / 1000
        return jwtTimestamp < changedTime
    # false means not changed
    return False


def createPasswordResetToken():
    resetToken = Random.get_random_bytes(
        32)
    password_reset_token = Hash.SHA256.new(
    ).update(resetToken).hexdigest()
    password_reset_expire = datetime.datetime.now(
    ).microsecond + 10 * 60 * 1000

    return {resetToken, password_reset_token, password_reset_expire}
