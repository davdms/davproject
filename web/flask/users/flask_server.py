from flask import Flask
from flask import request
from flask import render_template
import psycopg2
import sys
import requests
import csv

app = Flask(__name__)

@app.route("/")
def mainpage():
    return render_template('home.html')

@app.route("/registr")
def registr():
    response = "<p>Registration</p>"
    return response

# @app.route("/users")
# def users():
#     # response = "<p>Users</p>"
#     conn = psycopg2.connect("dbname=web_db_1 user=postgres password=barevp host=localhost")
#     cur = conn.cursor()
#     cur.execute('select id, email from users')
#     answer = cur.fetchone()
#     response = f"<p>Users<br><br> {answer}</p>"
#     return response

@app.route("/users")
def users():
    file = open("MOCK_DATA.csv")
    csvreader = csv.reader(file)
    header = next(csvreader)
    rows = []
    for row in csvreader:
        rows.append(row)
    file.close()
    return f"<p>{rows}</p>"


@app.route("/users/<id>")
def user(id):
    file = open("MOCK_DATA.csv")
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        if row[0] == id:
            return f"<p>{row}</p>"

if __name__ == "__main__":
    app.run()