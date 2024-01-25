# Name: Eduardo Manuel Costa Moreira
# Student ID: MOR21500097
# Date: 17/01/2024
from flask import Flask, jsonify, request, send_file
import random
from cryptography.fernet import Fernet

app = Flask(__name__)


def generateKey(data):
    data = bytes(str(data), 'utf-8')  # Convert the data into string then convert it into bytes
    key = Fernet.generate_key()  # Generate the key that is the only thing that can encrypt/decrypt the data
    data_key = Fernet(key)  # Put the key into a fernet in the data_key variable, the message that gets
    # encrypted with this key cannot be seen unless decrypted with this key
    token = data_key.encrypt(data)  # Encrypt the data using the key into the token variable
    return token, key  # return the token which contains the data and the data_key which contains the key


@app.route('/secure-api/say-hi', methods=['GET']) # Set up a URL route where it will take a function
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


if __name__ == '__main__':
    app.run(debug=True, port=8000)