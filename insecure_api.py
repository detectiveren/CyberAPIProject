# Name: Eduardo Manuel Costa Moreira
# Student ID: MOR21500097
# Date: 17/01/2024
from flask import Flask, jsonify, request, send_file, redirect, render_template
from flask_cors import CORS, cross_origin
import random
import sqlite3

# Deployable on Windows, Mac and Linux

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# These app routes below are for the web pages that will interact with the API

# Insecure API Web Page Routes


@app.route('/')
@cross_origin()
def homePage():
    print("User is accessing home page")
    return render_template('index.html')


@app.route('/insecure/sayhello')
@cross_origin()
def sayHelloPage():
    print("User is accessing Hello Page for Insecure API")
    return render_template('/html/insecure/sayhello.html')


@app.route('/insecure/ageprediction')
@cross_origin()
def agePredictionPage():
    print("User is accessing Age Prediction Page for Insecure API")
    return render_template('/html/insecure/ageprediction.html')


@app.route('/insecure/email')
@cross_origin()
def emailPage():
    print("User is accessing Email Login Page for Insecure API")
    return render_template('/html/insecure/emailLogIn.html')


@app.route('/insecure/sampleSensitiveData')
@cross_origin()
def sampleSensitiveDataPage():
    print("User is accessing Sample Sensitive Data Page for Insecure API")
    return render_template('html/insecure/sampleSensitiveData.html')


@app.route('/insecure/sqlData')
@cross_origin()
def sampleSQLData():
    print("User is accessing SQLData Page for Insecure API")
    return render_template('html/insecure/sqldata.html')


@app.route('/insecure/sqlUserPosts')
@cross_origin()
def sampleUserPosts():
    print("User is accessing SQL User Posts Page for Insecure API")
    return render_template('html/insecure/retrieveuserposts.html')


# This app routes below are the API endpoints that the command line and web pages will interact with

@app.route('/unsecure-api/say-hi', methods=['GET'])  # Set up a URL route where it will take a function
@cross_origin()  # Allow for Cross Origin (this allows for CORS which modern browsers need)
def helloTest():
    name = request.args.get('name')  # get the name of the user from "?name="

    if name is None:
        text = 'Hello!'  # Put string "Hello" in text if there's no name

    else:
        text = 'Hello ' + name + '!'  # Put string of the user's name in text if there is one

    return text  # Display the outcome


@app.route('/unsecure-api/age-prediction', methods=['GET'])
@cross_origin()
def agePrediction():
    name = request.args.get('name')

    if name is None:
        text = "You didn't insert a name!"

    else:
        age = random.randint(0, 100)  # Generate a random number
        text = 'Hello ' + name + "!" + " Your predicted age is: " + str(age)  # Print out the full text

    return text


@app.route('/unsecure-api/email', methods=['GET'])
@cross_origin()
def emailLogIn():
    email = request.args.get('email')

    response = ""

    # Connect to database

    conn = sqlite3.connect('userdata_insecure.db')

    # Create cursor

    getEmailData = conn.cursor()

    # Query the database

    try:
        # Retrieve the email and username where the email matches what the user entered
        getEmailData.execute(f'SELECT email, username, id FROM userdata WHERE email=\'{email}\'')
        rows = getEmailData.fetchall()

        if rows:
            for row in rows:
                username = str(row[1])
                id = str(row[2])

                response = "Successfully logged in as: " + username + "<br>Here are your posts<br><br>"

                getEmailData.execute(
                    f'SELECT posts.post FROM posts INNER JOIN userdata ON posts.userdata_id = '
                    f'userdata.id WHERE posts.userdata_id={id}')
                rows = getEmailData.fetchall()
                for row in rows:
                    for i in range(len(row)):
                        response += f"Post: {row[i]}<br>"  # Print out the text in the row alongside the column name
                    response += "<br>"
        else:
            response = "No account with that email was found on the database"
    except:
        response = "Error with database"

    return response


@app.route('/unsecure-api/sampleData', methods=['GET'])
@cross_origin()
def sampleData():
    sampleDataFile = request.args.get('sampleDataNumber')  # Grab the number input

    sampleDataFileNumber = int(sampleDataFile)  # Convert it into an integer

    try:
        with open("data/sampleData.txt", "r") as f:  # Open the text file containing the sample data
            for i, line in enumerate(f, 1):
                if i == sampleDataFileNumber:  # If i equals the number from sampleDataFileNumber, return the line
                    response = line

                    return response
    except ValueError:
        response = "Something went wrong with the API"

        return response

    response = "Searched the text database and nothing was found"  # If nothing was found then return this variable

    return response


@app.route('/unsecure-api/grabSQLdata', methods=['GET'])
@cross_origin()
def getSQLiteData():
    # Error message if it the SQL database fails for some reason
    response = ""
    # Connect to the userdata db
    conn = sqlite3.connect('userdata_insecure.db')

    # Create cursor object
    cur = conn.cursor()

    # Query the database
    cur.execute('SELECT * FROM userdata')
    rows = cur.fetchall()

    # Get column names
    column_names = [description[0] for description in cur.description]

    for row in rows:
        for i in range(len(row)):
            response += f"{column_names[i]}: {row[i]}<br>"
        response += "<br>"
    return response


@app.route('/unsecure-api/grabUserPosts', methods=['GET'])
@cross_origin()
def grabUserPosts():
    userID = request.args.get('userID')  # Grab the user id

    randomUserID = int(userID)

    response = ""

    # Connect to the database
    conn = sqlite3.connect('userdata_insecure.db')

    # Create cursor object

    getUserData = conn.cursor()

    # Query the database

    getUserData.execute(
        f'SELECT userdata.username, posts.post FROM posts INNER JOIN userdata ON posts.userdata_id = userdata.id WHERE posts.userdata_id={randomUserID}')
    rows = getUserData.fetchall()

    column_names = [description[0] for description in getUserData.description]

    for row in rows:
        for i in range(len(row)):
            response += f"{column_names[i]}: {row[i]}<br>"  # Print out the text in the row alongside the column name
        response += "<br>"

    return response


# Re-route all of these when deploying to linux
# app.run(debug=True, host='10.0.2.5', port=8000) for example
if __name__ == '__main__':  # This is where the app begins
    app.run(debug=True, host='10.0.2.5', port=8000)
