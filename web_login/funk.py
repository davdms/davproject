import json
import csv
from csv import writer
import hashlib

def get_all_users():
    all_users = []
    with open('users.csv') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        for user in reader:
            all_users.append({'id': int(user[0]), 'username': user[1], 'password': user[2]})
    csvfile.close()
    return all_users

def get_user_by_username(username=None):
    all_users = get_all_users()
    for user in all_users:
        if user['username'] == username:
            return user

def get_new_userid():
    newuserid = 1
    all_users = get_all_users()
    for user in all_users:
        if user['id'] == newuserid:
            newuserid += 1
    return newuserid

def registr_new_user(username, password):
    newuserid = get_new_userid()
    newuser = [newuserid, username, password]
    write_in_users(newuser)

def write_in_users(newuser):
    with open('users.csv', 'a', newline='') as userscsv:
        writer_object = writer(userscsv)
        writer_object.writerow(newuser)
    userscsv.close()

def password_hashing(password):
    salt = 'qwertyui'
    if password:
        newpas = salt + password
        hashpass = hashlib.sha256(newpas.encode()).hexdigest()
        return hashpass

def username_check(username):
    name_error = [' ', '/', ',', '[', ']', '*', '#', '@']
    if username:
        for simb in name_error:
            if simb in username:
                return False
    return True
