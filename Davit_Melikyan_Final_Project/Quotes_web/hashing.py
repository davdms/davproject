import hashlib
from datetime import datetime


def hashing(name):
    salt = bytes('qwt', 'utf-8')
    dk = hashlib.pbkdf2_hmac('sha256', bytes(name, 'utf-8'), salt, 1000)
    return dk.hex()


def filenamehashing(name):
    namelist = name.rsplit('.')
    filename = namelist[0]
    fileformat = namelist[1]
    nowtime = str(datetime.now())
    salt = bytes('qwt', 'utf-8')
    dk = hashlib.pbkdf2_hmac('sha256', bytes(filename + nowtime, 'utf-8'), salt, 1000)
    hashname = dk.hex() + '.' + fileformat
    return hashname

