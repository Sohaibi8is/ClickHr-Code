import os
from flask import Flask, request, render_template
from flask import jsonify
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
  host="localhost",
  user="username",
  password="password",
  database = "dbname"
)

cursor = mydb.cursor()

# login api
@app.route("/api/login", methods=['POST'])
def login():

    # get name and password from user
    name = request.form["name"]
    password = request.form["password"]

    # select data from db
    query = "SELECT username , password FROM user;"
    cursor.execute(query)
    result = cursor.fetchall()

    #  if username and password exist in db then response "you are sucessfully login"
    #  If username or password(one is correct and one is incorrect) is not in db then response "name or password is incorrect"
    # else response "no user found"

    for i in result:
        if i[0]==name and i[1] == password:
            message = "you are sucessfully login " + name
            return jsonify({"status": 200, "message": message})

        if i[0] == name or i[1] == password:
            message = "name or password is incorrect "
            return jsonify({"status": 400, "message": message})

    else:
        message = "no user found " + name
        return jsonify({"status": 400, "message": message})


# signup api
@app.route("/api/signup", methods=['POST'])
def signup():

    # get name and password from user
    name = request.form["name"]
    password = request.form["password"]

    # if username and password are not empty then input it in database
    # else respone "invalid data"

    if name and password:
        query = "INSERT INTO user(username, password) VALUES (%s , %s);"
        values = (name, password)
        cursor.execute(query, values)
        mydb.commit()

        message = "User is added suceesfully."
        return jsonify({"status": 200, "messages":message})

    else:
        message = "Invalid data"
        return jsonify({"status": 400, "messages": message})

# forget password api -> pass username with url
@app.route("/api/forget_password/<name>", methods=['POST'])
def forget_password(name):

    # save name and get password input from user
    u_name = name
    password = request.form["password"]

    query1 = "SELECT * FROM user;"
    cursor.execute(query1)
    result = cursor.fetchall()

    # if user exist in db then update the password
    # else response "Unknown user"
    for i in result:
        if i[1] == u_name:
            username = i[1]
            if username and password:
                query = "UPDATE user SET password = %s WHERE username = %s;"
                values = (password, username)
                cursor.execute(query, values)
                mydb.commit()

                message = "Password updated suceesfully."
                return jsonify({"status": 200, "messages":message})

    else:
        message = "Unknown User"
        return jsonify({"status": 400, "messages": message})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

    host = ''