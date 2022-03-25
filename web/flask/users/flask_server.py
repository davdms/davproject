from flask import Flask
from flask import request
from flask import render_template
import psycopg2
import sys

app = Flask(__name__)

@app.route("/")
def mainpage():
    return render_template('home.html')

@app.route("/registr")
def registr():
    response = "<p>Registration</p>"
    return response

@app.route("/users")
def users():
    response = "<p>Users</p>"
    return response

# @app.route("/users")
# def users():
#     answer = []
#     with open('MOCK_DATA.csv', 'r') as f:
#         for line in f.readlines():
#             answer.append(line)
#     return answer


@app.route("/users/<id>")
def user(id):
    response = f"<p>User information {id}</p>"
    return response

if __name__ == "__main__":
    app.run()