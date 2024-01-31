# Name: Eduardo Manuel Costa Moreira
# Student ID: MOR21500097
# Date: 31/01/2024
from flask import Flask, jsonify, request, send_file, render_template
from flask_cors import CORS, cross_origin
import random
from cryptography.fernet import Fernet

# DO NOT FORGET TO ADD CORS TO THIS API

app = Flask(__name__)


def generateKey(data):
    data = bytes(str(data), 'utf-8')  # Convert the data into string then convert it into bytes
    key = Fernet.generate_key()  # Generate the key that is the only thing that can encrypt/decrypt the data
    data_key = Fernet(key)  # Put the key into a fernet in the data_key variable, the message that gets
    # encrypted with this key cannot be seen unless decrypted with this key
    token = data_key.encrypt(data)  # Encrypt the data using the key into the token variable
    return token, key  # return the token which contains the data and the data_key which contains the key


# These app routes below are for the web pages that will interact with the API

# Secure API Web Page Routes

@app.route('/')
@cross_origin()
def homePage():
    return render_template('index.html')


@app.route('/secure/sayhello')
@cross_origin()
def sayHelloPage():
    return render_template('/html/secure/sayhello.html')


@app.route('/secure/ageprediction')
@cross_origin()
def agePredictionPage():
    return render_template('/html/secure/ageprediction.html')


@app.route('/secure/email')
@cross_origin()
def emailPage():
    return render_template('/html/secure/emailLogin.html')


@app.route('/secure/sampleSensitiveData')
@cross_origin()
def sampleDataPage():
    return render_template('/html/secure/sampleSensitiveData.html')


# This app routes below are the API endpoints that the command line and web pages will interact with

@app.route('/secure-api/say-hi', methods=['GET']) # Set up a URL route where it will take a function
@cross_origin()
def helloTest():
    name = request.args.get('name') # get the name of the user from "?name="

    if name is None:
        response = "Hello!" # Put the string "Hello" in response
        data = generateKey(response) # Encrypt the message
        text = [str(data[0]), str(data[1])]

    else:
        response = 'Hello ' + name + '!' # Put the string along with the name in the response variable
        data = generateKey(response)
        text = [str(data[0]), str(data[1])]

    return jsonify({"Token" : str(data[0]), "Key" : str(data[1])})


@app.route('/secure-api/age-prediction', methods=['GET'])
@cross_origin()
def agePrediction():
    name = request.args.get('name')

    if name is None:
        response = "You didn't insert a name!"
        data = generateKey(response)

    else:
        age = random.randint(0, 100) # Generate a random number
        response = 'Hello ' + name + "!" + " Your predicted age is: " + str(age)
        data = generateKey(response)

    return jsonify({"Token" : str(data[0]), "Key" : str(data[1])})


@app.route('/secure-api/email', methods=['GET'])
@cross_origin()
def emailLogIn():
    email = request.args.get('email')
    if email is None:
        response = "You didn't input an email, invalid login"
        data = generateKey(response)

    elif email == "eddy@gmail.com":
        response = "You have logged in successfully to " + email
        data = generateKey(response)

    else:
        response = "The email " + email + " is not found on the database"
        data = generateKey(response)

    return jsonify({"Token" : str(data[0]), "Key" : str(data[1])})


@app.route('/secure-api/sampleData', methods=['GET'])
@cross_origin()
def sampleData():
    sampleDataFile = request.args.get('sampleDataNumber') # Grab the number input

    sampleDataFileNumber = int(sampleDataFile) # Convert it into an integer

    try:
        with open("data/sampleData.txt", "r") as f: # Open the text file containing the sample data
            for i, line in enumerate(f, 1):
                if i == sampleDataFileNumber: # If i equals the number from sampleDataFileNumber, return the line
                    response = line
                    data = generateKey(response)
                    return jsonify({"Token" : str(data[0]), "Key" : str(data[1])})
    except ValueError:
        response = "Something went wrong with the API"
        data = generateKey(response)
        return jsonify({"Token" : str(data[0]), "Key" : str(data[1])})

    response = "Searched the text database and nothing was found" # If nothing was found then return this variable
    data = generateKey(response)
    return jsonify({"Token" : str(data[0]), "Key" : str(data[1])})


# Re-route all of these when deploying to linux
# app.run(debug=True, host='10.0.2.4', port=8000) for example
if __name__ == '__main__':
    app.run(debug=True, port=8000)