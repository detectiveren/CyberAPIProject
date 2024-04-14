# Name: Eduardo Manuel Costa Moreira
# Student ID: MOR21500097
# Date: 17/01/2024
from flask import Flask, jsonify, request, send_file, redirect, render_template
from flask_cors import CORS, cross_origin
import random

# Deployable on Windows, Mac and Linux

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# These app routes below are for the web pages that will interact with the API

# Insecure API Web Page Routes


@app.route('/')
@cross_origin()
def homePage():
    return render_template('index.html')


@app.route('/insecure/sayhello')
@cross_origin()
def sayHelloPage():
    return render_template('/html/insecure/sayhello.html')


@app.route('/insecure/ageprediction')
@cross_origin()
def agePredictionPage():
    return render_template('/html/insecure/ageprediction.html')


@app.route('/insecure/email')
@cross_origin()
def emailPage():
    return render_template('/html/insecure/emailLogIn.html')


@app.route('/insecure/sampleSensitiveData')
@cross_origin()
def sampleSensitiveDataPage():
    return render_template('html/insecure/sampleSensitiveData.html')


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

    if email_account == "eddy@gmail.com":  # If the login is valid
        text = "You have logged in successfully to " + email_account
        return text
    else:
        return redirect('/unsecure-api/email?email=' + email_account, code=302)  # If the login is invalid


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


# Re-route all of these when deploying to linux
# app.run(debug=True, host='10.0.2.5', port=8000) for example
if __name__ == '__main__':  # This is where the app begins
    app.run(debug=True, port=8000)
