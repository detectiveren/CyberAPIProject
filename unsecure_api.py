# Name: Eduardo Manuel Costa Moreira
# Student ID: MOR21500097
# Date: 17/01/2024
from flask import Flask, jsonify, request, send_file, redirect
from flask_cors import CORS, cross_origin
import random

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/unsecure-api/say-hi', methods=['GET'])  # Set up a URL route where it will take a function
@cross_origin() # Allow for Cross Origin (this allows for CORS which modern browsers need)
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

    if email == "":
        text = "You didn't input an email, invalid login"
        return text

    elif email == "eddy@gmail.com":
        return redirect('/unsecure-api/email_account?emailAccount=' + email, code=302)

    else:
        text = "The email " + email + " is not found on the database"
        return text


@app.route('/unsecure-api/email_account', methods=['GET'])
@cross_origin()
def loggedIn():
    email_account = request.args.get('emailAccount')

    if email_account == "eddy@gmail.com": # If the login is valid
        text = "You have logged in successfully to " + email_account
        return text
    else:
        return redirect('/unsecure-api/email?email=' + email_account, code=302) # If the login is invalid


if __name__ == '__main__':  # This is where the app begins
    app.run(debug=True, port=8000)
