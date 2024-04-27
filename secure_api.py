# Name: Eduardo Manuel Costa Moreira
# Student ID: MOR21500097
# Date: 22/02/2024
from flask import Flask, jsonify, request, send_file, render_template
from flask_cors import CORS, cross_origin
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad
import random, base64
import sqlite3

# Deployable on Windows, Mac and Linux

# DO NOT FORGET TO ADD CORS TO THIS API

app = Flask(__name__)


# Fernet will no longer be used as JavaScript does not support it properly, therefore the change to AES
# encryption and decryption was necessary

# This API has SQL Injection Prevention which means it is built to prevent SQL Injection Attacks

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
    print("User is accessing home page")
    return render_template('index.html')


@app.route('/secure/sayhello')
@cross_origin()
def sayHelloPage():
    print("User is accessing Hello Page for Secure API")
    return render_template('/html/secure/sayhello.html')


@app.route('/secure/ageprediction')
@cross_origin()
def agePredictionPage():
    print("User is accessing Age Prediction Page for Secure API")
    return render_template('/html/secure/ageprediction.html')


@app.route('/secure/email')
@cross_origin()
def emailPage():
    print("User is accessing Email Login Page for Secure API")
    return render_template('/html/secure/emailLogIn.html')


@app.route('/secure/sampleSensitiveData')
@cross_origin()
def sampleDataPage():
    print("User is accessing Sample Sensitive Data Page for Secure API")
    return render_template('/html/secure/sampleSensitiveData.html')


@app.route('/secure/sqlData')
@cross_origin()
def sampleSQLData():
    print("User is accessing SQLData Page for Secure API")
    return render_template('html/secure/sqldata.html')


@app.route('/secure/sqlUserPosts')
@cross_origin()
def sampleUserPosts():
    print("User is accessing SQL User Posts Page for Secure API")
    return render_template('html/secure/retrieveuserposts.html')


# This app routes below are the API endpoints that the command line and web pages will interact with

@app.route('/secure-api/say-hi', methods=['GET'])  # Set up a URL route where it will take a function
@cross_origin()
def helloTest():
    encrypted_name = request.args.get('name')  # get the name of the user from "?name="
    iv = request.args.get('iv')

    key = b'01234567890123456789012345678901'  # The secret key, it must be the exact same as the key on the JS Script
    # Decrypt the name using AES
    cipher = AES.new(key, AES.MODE_CBC, base64.b64decode(iv))
    decrypted_name = unpad(cipher.decrypt(base64.b64decode(encrypted_name)), AES.block_size).decode('utf-8')

    name = str(decrypted_name)

    if name is None:
        response = "Hello!"  # Put the string "Hello" in response

    else:
        response = 'Hello ' + name + '!'  # Put the string along with the name in the response variable

    encrypted_data_b64, key_b64 = newGenerateKey(response)

    return jsonify({"Token": encrypted_data_b64, "Key": key_b64})


@app.route('/secure-api/age-prediction', methods=['GET'])
@cross_origin()
def agePrediction():
    encrypted_name = request.args.get('name')
    iv = request.args.get('iv')

    key = b'01234567890123456789012345678901'  # The secret key, it must be the exact same as the key on the JS Script
    # Decrypt the name using AES
    cipher = AES.new(key, AES.MODE_CBC, base64.b64decode(iv))
    decrypted_name = unpad(cipher.decrypt(base64.b64decode(encrypted_name)), AES.block_size).decode('utf-8')

    name = str(decrypted_name)

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
    encrypted_email = request.args.get('email')
    iv = request.args.get('iv')

    key = b'01234567890123456789012345678901'  # The secret key, it must be the exact same as the key on the JS Script
    # Decrypt the email using AES
    cipher = AES.new(key, AES.MODE_CBC, base64.b64decode(iv))
    decrypted_email = unpad(cipher.decrypt(base64.b64decode(encrypted_email)), AES.block_size).decode('utf-8')

    email = decrypted_email
    sql_injection_prevention = ['\'--', '\' true--', '\'', "\' OR \'1\'=\'1\' --", "\'; DROP TABLE userdata; --",
                                "\'; DROP TABLE posts; --", ";", "--"]
    # List of strings that are used in SQL Injection Attacks

    if any(sql_injection_type in email for sql_injection_type in sql_injection_prevention):
        # If those SQL Injection strings are found, tell the API that an attempt was made and that it was blocked
        # by resetting the value to "0" or "invalid"
        print("SQL INJECTION ATTEMPT BLOCKED")
        print("Attempted input: " + email)
        email = "invalid"
        print("Value for email was reset to: " + email)

    response = ""

    # Connect to database

    conn = sqlite3.connect('userdata_secure.db')

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


@app.route('/secure-api/grabSQLdata', methods=['GET'])  # User SQL database
@cross_origin()
def getSQLiteData():
    sqlDataNumber = request.args.get('sqlNumber')  # Grab the number input
    sql_injection_prevention = ['\'--', '\' true--', '\'', "\' OR \'1\'=\'1\' --", "\'; DROP TABLE userdata; --",
                                "\'; DROP TABLE posts; --", ";", "--"]
    # List of strings that are used in SQL Injection Attacks

    if any(sql_injection_type in sqlDataNumber for sql_injection_type in sql_injection_prevention):
        # If those SQL Injection strings are found, tell the API that an attempt was made and that it was blocked
        # by resetting the value to "0" or "invalid"
        print("SQL INJECTION ATTEMPT BLOCKED")
        print("Attempted input: " + sqlDataNumber)
        sqlDataNumber = "0"
        print("Value for sqlDataNumber was reset to: " + sqlDataNumber)

    randomNumber = int(sqlDataNumber)
    # Error message if it is the SQL database fails for some reason
    response = ""
    # Connect to the userdata db
    conn = sqlite3.connect('userdata_secure.db')

    # Create cursor object
    cur = conn.cursor()

    # Query the database
    cur.execute(f'SELECT * FROM userdata WHERE id={randomNumber}')
    rows = cur.fetchall()

    # Get column names
    column_names = [description[0] for description in cur.description]

    for row in rows:
        for i in range(len(row)):
            response += f"{column_names[i]}: {row[i]} \n <br>"  # Print out the text in the row alongside the column name

    encrypted_data_b64, key_b64 = newGenerateKey(response)
    return jsonify({"Token": encrypted_data_b64, "Key": key_b64})


@app.route('/secure-api/grabUserPosts', methods=['GET'])
@cross_origin()
def grabUserPosts():
    userID = request.args.get('userID')  # Grab the user id
    sql_injection_prevention = ['\'--', '\' true--', '\'', "\' OR \'1\'=\'1\' --", "\'; DROP TABLE userdata; --",
                                "\'; DROP TABLE posts; --", ";", "--"]
    # List of strings that are used in SQL Injection Attacks

    if any(sql_injection_type in userID for sql_injection_type in sql_injection_prevention):
        # If those SQL Injection strings are found, tell the API that an attempt was made and that it was blocked
        # by resetting the value to "0" or "invalid"
        print("SQL INJECTION ATTEMPT BLOCKED")
        print("Attempted input: " + userID)
        userID = "0"
        print("Value for userID was reset to: " + userID)

    randomUserID = int(userID)

    response = ""

    # Connect to the database
    conn = sqlite3.connect('userdata_secure.db')

    # Create cursor object

    getUserData = conn.cursor()

    # Query the database

    getUserData.execute(f'SELECT userdata.username, posts.post FROM posts INNER JOIN userdata ON posts.userdata_id = userdata.id WHERE posts.userdata_id={randomUserID}')
    rows = getUserData.fetchall()

    column_names = [description[0] for description in getUserData.description]

    for row in rows:
        for i in range(len(row)):
            response += f"{column_names[i]}: {row[i]} \n <br>"  # Print out the text in the row alongside the column name

    encrypted_data_b64, key_b64 = newGenerateKey(response)
    return jsonify({"Token": encrypted_data_b64, "Key": key_b64})


# Re-route all of these when deploying to linux
# app.run(debug=True, host='10.0.2.5', port=8000) for example
if __name__ == '__main__':
    app.run(debug=True, host='10.0.2.5', port=9000)
