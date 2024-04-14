# Name: Eduardo Manuel Costa Moreira
# Student ID: MOR21500097
# Date: 22/02/2024
from flask import Flask, jsonify, request, send_file, render_template
from flask_cors import CORS, cross_origin
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import random, base64

# Deployable on Windows, Mac and Linux

# DO NOT FORGET TO ADD CORS TO THIS API

app = Flask(__name__)


# Fernet will no longer be used as JavaScript does not support it properly, therefore the change to AES
# encryption and decryption was necessary

def newGenerateKey(data):
    data = bytes(str(data), 'utf-8')
    key = get_random_bytes(16)  # Generate a 16-byte (128-bit) AES key
    cipher = AES.new(key, AES.MODE_ECB)  # Create an AES cipher object in ECB mode
    # Pad the data to be a multiple of 16 bytes (AES block size)
    padded_data = data + b"\0" * (AES.block_size - len(data) % AES.block_size)
    # Encrypt the padded data using AES
    encrypted_data = cipher.encrypt(padded_data)
    # Base64 encode the encrypted data and key
    encrypted_data_b64 = base64.b64encode(encrypted_data).decode('utf-8')
    key_b64 = base64.b64encode(key).decode('utf-8')
    return encrypted_data_b64, key_b64


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

@app.route('/secure-api/say-hi', methods=['GET'])  # Set up a URL route where it will take a function
@cross_origin()
def helloTest():
    name = request.args.get('name')  # get the name of the user from "?name="

    if name is None:
        response = "Hello!"  # Put the string "Hello" in response

    else:
        response = 'Hello ' + name + '!'  # Put the string along with the name in the response variable

    encrypted_data_b64, key_b64 = newGenerateKey(response)

    return jsonify({"Token": encrypted_data_b64, "Key": key_b64})


@app.route('/secure-api/age-prediction', methods=['GET'])
@cross_origin()
def agePrediction():
    name = request.args.get('name')

    if name is None:
        response = "You didn't insert a name!"

    else:
        age = random.randint(0, 100)  # Generate a random number
        response = 'Hello ' + name + "!" + " Your predicted age is: " + str(age)

    encrypted_data_b64, key_b64 = newGenerateKey(response)

    return jsonify({"Token": encrypted_data_b64, "Key": key_b64})


@app.route('/secure-api/email', methods=['GET'])
@cross_origin()
def emailLogIn():
    email = request.args.get('email')
    if email is None:
        response = "You didn't input an email, invalid login"

    elif email == "eddy@gmail.com":
        response = "You have logged in successfully to " + email

    else:
        response = "The email " + email + " is not found on the database"

    encrypted_data_b64, key_b64 = newGenerateKey(response)

    return jsonify({"Token": encrypted_data_b64, "Key": key_b64})


@app.route('/secure-api/sampleData', methods=['GET'])
@cross_origin()
def sampleData():
    sampleDataFile = request.args.get('sampleDataNumber')  # Grab the number input

    sampleDataFileNumber = int(sampleDataFile)  # Convert it into an integer

    try:
        with open("data/sampleData.txt", "r") as f:  # Open the text file containing the sample data
            for i, line in enumerate(f, 1):
                if i == sampleDataFileNumber:  # If i equals the number from sampleDataFileNumber, return the line
                    response = line
                    encrypted_data_b64, key_b64 = newGenerateKey(response)

                    return jsonify({"Token": encrypted_data_b64, "Key": key_b64})
    except ValueError:
        response = "Something went wrong with the API"
        encrypted_data_b64, key_b64 = newGenerateKey(response)

        return jsonify({"Token": encrypted_data_b64, "Key": key_b64})

    response = "Searched the text database and nothing was found"  # If nothing was found then return this variable
    encrypted_data_b64, key_b64 = newGenerateKey(response)

    return jsonify({"Token": encrypted_data_b64, "Key": key_b64})


# Re-route all of these when deploying to linux
# app.run(debug=True, host='10.0.2.4', port=8000) for example
if __name__ == '__main__':
    app.run(debug=True, port=8000)
