# Name: Eduardo Manuel Costa Moreira
# Student ID: MOR21500097
# Date: 27/04/2024
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
    return render_template('/html/secure/emailVerify.html')


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


@app.route('/secure/accountAccess')
@cross_origin()
def accountAccess():
    print("User is accessing Account Access Page for Secure API")
    return render_template('html/secure/account_access.html')


@app.route('/secure/eraseData')
@cross_origin()
def eraseAccountData():
    print("User is accessing Erase Data for Secure API")
    return render_template('html/secure/erase_account_data.html')


# This app routes below are the API endpoints that the command line and web pages will interact with

@app.route('/secure-api/say-hi', methods=['GET'])  # Set up a URL route where it will take a function
@cross_origin()
def helloTest():
    try:
        encrypted_name = request.args.get('name')  # get the name of the user from "?name="
        iv = request.args.get('iv')
    except:
        encrypted_name = "undefined"
        iv = "undefined"

    key = b'01234567890123456789012345678901'  # The secret key, it must be the exact same as the key on the JS Script

    try:
        # Decrypt the name using AES
        cipher = AES.new(key, AES.MODE_CBC, base64.b64decode(iv))
        decrypted_name = unpad(cipher.decrypt(base64.b64decode(encrypted_name)), AES.block_size).decode('utf-8')
    except:
        decrypted_name = "undefined"

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
    try:
        encrypted_name = request.args.get('name')
        iv = request.args.get('iv')
    except:
        encrypted_name = "undefined"
        iv = "undefined"

    key = b'01234567890123456789012345678901'  # The secret key, it must be the exact same as the key on the JS Script

    try:
        # Decrypt the name using AES
        cipher = AES.new(key, AES.MODE_CBC, base64.b64decode(iv))
        decrypted_name = unpad(cipher.decrypt(base64.b64decode(encrypted_name)), AES.block_size).decode('utf-8')
    except:
        decrypted_name = "undefined"

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
def emailVerify():
    try:
        encrypted_email = request.args.get('email')
        iv = request.args.get('iv')
    except:
        encrypted_email = "undefined"
        iv = "undefined"

    key = b'01234567890123456789012345678901'  # The secret key, it must be the exact same as the key on the JS Script

    try:
        # Decrypt the email using AES
        cipher = AES.new(key, AES.MODE_CBC, base64.b64decode(iv))
        decrypted_email = unpad(cipher.decrypt(base64.b64decode(encrypted_email)), AES.block_size).decode('utf-8')
    except:
        decrypted_email = "undefined"

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
        getEmailData.execute(f'SELECT email FROM userdata WHERE email=\'{email}\'')
        rows = getEmailData.fetchall()

        if rows:
            for row in rows:
                email = str(row[0])

                response = "Successfully found email: " + email
        else:
            response = "No account with that email was found on the database"
    except:
        response = "Error with database"

    encrypted_data_b64, key_b64 = newGenerateKey(response)

    return jsonify({"Token": encrypted_data_b64, "Key": key_b64})


@app.route('/secure-api/sampleData', methods=['GET'])
@cross_origin()
def sampleData():
    try:
        sampleDataFile = request.args.get('sampleDataNumber')  # Grab the number input
    except:
        sampleDataFile = "0"

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
    try:
        encrypted_email = base64.b64decode(request.args.get('e'))
        encrypted_password = base64.b64decode(request.args.get('p'))
        encrypted_secret_answer = base64.b64decode(request.args.get('s'))
        encrypted_userID = base64.b64decode(request.args.get('id'))
        iv = base64.b64decode(request.args.get('iv'))
    except:
        encrypted_email = "undefined"
        encrypted_password = "undefined"
        encrypted_secret_answer = "undefined"
        encrypted_userID = "undefined"
        iv = "undefined"

    key = b'01234567890123456789012345678901'  # The secret key, it must be the exact same as the key on the JS Script

    try:
        # Decrypt the email and password using AES
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_email = unpad(cipher.decrypt(encrypted_email), AES.block_size).decode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_password = unpad(cipher.decrypt(encrypted_password), AES.block_size).decode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_secret_answer = unpad(cipher.decrypt(encrypted_secret_answer), AES.block_size).decode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_userID = unpad(cipher.decrypt(encrypted_userID), AES.block_size).decode('utf-8')
    except:
        decrypted_email = "undefined"
        decrypted_password = "undefined"
        decrypted_secret_answer = "undefined"
        decrypted_userID = "undefined"

    email = decrypted_email
    password = decrypted_password
    secret_answer = decrypted_secret_answer
    userID = decrypted_userID
    sql_injection_prevention = ['\'--', '\' true--', '\'', "\' OR \'1\'=\'1\' --", "\'; DROP TABLE userdata; --",
                                "\'; DROP TABLE posts; --", ";", "--"]
    # List of strings that are used in SQL Injection Attacks

    if any(sql_injection_type in email for sql_injection_type in sql_injection_prevention):
        # If those SQL Injection strings are found, tell the API that an attempt was made and that it was blocked
        # by resetting the value to "0" or "invalid"
        print("SQL INJECTION ATTEMPT BLOCKED")
        print("Attempted input: " + email)
        email = "Invalid"
        print("Value for email was reset to: " + email)

    if any(sql_injection_type in password for sql_injection_type in sql_injection_prevention):
        # If those SQL Injection strings are found, tell the API that an attempt was made and that it was blocked
        # by resetting the value to "0" or "invalid"
        print("SQL INJECTION ATTEMPT BLOCKED")
        print("Attempted input: " + password)
        password = "Invalid"
        print("Value for password was reset to: " + password)

    if any(sql_injection_type in secret_answer for sql_injection_type in sql_injection_prevention):
        # If those SQL Injection strings are found, tell the API that an attempt was made and that it was blocked
        # by resetting the value to "0" or "invalid"
        print("SQL INJECTION ATTEMPT BLOCKED")
        print("Attempted input: " + secret_answer)
        secret_answer = "invalid"
        print("Value for secret_answer was reset to: " + secret_answer)

    if any(sql_injection_type in userID for sql_injection_type in sql_injection_prevention):
        # If those SQL Injection strings are found, tell the API that an attempt was made and that it was blocked
        # by resetting the value to "0" or "invalid"
        print("SQL INJECTION ATTEMPT BLOCKED")
        print("Attempted input: " + userID)
        userID = "0"
        print("Value for userID was reset to: " + userID)

    # Error message if it is the SQL database fails for some reason
    response = ""
    # Connect to the userdata db
    conn = sqlite3.connect('userdata_secure.db')

    # Create cursor object
    cur = conn.cursor()

    try:
        # Retrieve the email and username where the email matches what the user entered
        cur.execute(
            f'SELECT id FROM userdata WHERE email=\'{email}\' AND password =\'{password}\' AND secret_answer=\'{secret_answer}\'')
        rows = cur.fetchall()

        if rows:
            for row in rows:
                loggedInUserID = str(row[0])
                cur.execute(f'SELECT EXISTS (SELECT 1 FROM admin WHERE userdata_id = ?)', (loggedInUserID,))
                isUserAdmin = cur.fetchone()[0]

                if isUserAdmin:
                    # Query the database
                    cur.execute(f'SELECT * FROM userdata WHERE id={userID}')
                    rows = cur.fetchall()

                    # Get column names
                    column_names = [description[0] for description in cur.description]

                    for row in rows:
                        for i in range(len(row)):
                            response += f"{column_names[i]}: {row[i]} \n <br>"  # Print out the text in the row alongside the column name
                else:
                    response = "User is not admin and therefore has no access to this information"

        else:
            response = "No account with that email and/or password was found on the database"
    except sqlite3.Error as e:
        response = "Error with database"
        print(e)

    encrypted_data_b64, key_b64 = newGenerateKey(response)
    return jsonify({"Token": encrypted_data_b64, "Key": key_b64})


@app.route('/secure-api/grabUserPosts', methods=['GET'])
@cross_origin()
def grabUserPosts():
    try:
        userID = request.args.get('userID')  # Grab the user id
    except:
        userID = "0"
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

    getUserData.execute(
        f'SELECT userdata.username, posts.post FROM posts INNER JOIN userdata ON posts.userdata_id = userdata.id WHERE posts.userdata_id={randomUserID}')
    rows = getUserData.fetchall()

    column_names = [description[0] for description in getUserData.description]

    for row in rows:
        for i in range(len(row)):
            response += f"{column_names[i]}: {row[i]} \n <br>"  # Print out the text in the row alongside the column name

    encrypted_data_b64, key_b64 = newGenerateKey(response)
    return jsonify({"Token": encrypted_data_b64, "Key": key_b64})


@app.route('/secure-api/accountAccessPortal', methods=['GET'])
@cross_origin()
def accessAccountPortal():
    try:
        encrypted_email = base64.b64decode(request.args.get('e'))
        encrypted_password = base64.b64decode(request.args.get('p'))
        encrypted_secret_answer = base64.b64decode(request.args.get('s'))
        iv = base64.b64decode(request.args.get('iv'))
    except:
        encrypted_email = "undefined"
        encrypted_password = "undefined"
        encrypted_secret_answer = "undefined"
        iv = "undefined"

    key = b'01234567890123456789012345678901'  # The secret key, it must be the exact same as the key on the JS Script
    # Decrypt the email and password using AES
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_email = unpad(cipher.decrypt(encrypted_email), AES.block_size).decode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_password = unpad(cipher.decrypt(encrypted_password), AES.block_size).decode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_secret_answer = unpad(cipher.decrypt(encrypted_secret_answer), AES.block_size).decode('utf-8')
    except:
        decrypted_email = "undefined"
        decrypted_password = "undefined"
        decrypted_secret_answer = "undefined"

    email = decrypted_email
    password = decrypted_password
    secret_answer = decrypted_secret_answer
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

    if any(sql_injection_type in password for sql_injection_type in sql_injection_prevention):
        # If those SQL Injection strings are found, tell the API that an attempt was made and that it was blocked
        # by resetting the value to "0" or "invalid"
        print("SQL INJECTION ATTEMPT BLOCKED")
        print("Attempted input: " + password)
        password = "invalid"
        print("Value for password was reset to: " + password)

    if any(sql_injection_type in secret_answer for sql_injection_type in sql_injection_prevention):
        # If those SQL Injection strings are found, tell the API that an attempt was made and that it was blocked
        # by resetting the value to "0" or "invalid"
        print("SQL INJECTION ATTEMPT BLOCKED")
        print("Attempted input: " + secret_answer)
        secret_answer = "invalid"
        print("Value for secret answer was reset to: " + secret_answer)

    response = ""

    # Connect to database

    conn = sqlite3.connect('userdata_secure.db')

    # Create cursor

    getAccountData = conn.cursor()

    # Query the database

    try:
        # Retrieve the email and username where the email matches what the user entered
        getAccountData.execute(
            f'SELECT email, username, id FROM userdata WHERE email=\'{email}\' AND password =\'{password}\' AND secret_answer=\'{secret_answer}\'')
        rows = getAccountData.fetchall()

        if rows:
            for row in rows:
                username = str(row[1])
                id = str(row[2])

                response = "Successfully logged in as: " + username + "<br>Here are your posts<br><br>"

                getAccountData.execute(
                    f'SELECT posts.post FROM posts INNER JOIN userdata ON posts.userdata_id = '
                    f'userdata.id WHERE posts.userdata_id={id}')
                rows = getAccountData.fetchall()
                for row in rows:
                    for i in range(len(row)):
                        response += f"Post: {row[i]}<br>"  # Print out the text in the row alongside the column name
                    response += "<br>"
        else:
            response = "No account with that email and/or password was found on the database"
    except:
        response = "Error with database"

    encrypted_data_b64, key_b64 = newGenerateKey(response)

    print(str(jsonify({"Token": encrypted_data_b64, "Key": key_b64})))

    return jsonify({"Token": encrypted_data_b64, "Key": key_b64})


@app.route('/secure-api/eraseDataPortal', methods=['GET'])
@cross_origin()
def eraseDataPortal():
    try:
        encrypted_email = base64.b64decode(request.args.get('e'))  # Grabbing the values from the parameters
        encrypted_password = base64.b64decode(request.args.get('p'))
        encrypted_secret_answer = base64.b64decode(request.args.get('s'))
        iv = base64.b64decode(request.args.get('iv'))
    except:
        encrypted_email = "undefined"
        encrypted_password = "undefined"
        encrypted_secret_answer = "undefined"
        iv = "undefined"

    key = b'01234567890123456789012345678901'  # The secret key, it must be the exact same as the key on the JS Script
    # Decrypt the email and password using AES
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_email = unpad(cipher.decrypt(encrypted_email), AES.block_size).decode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_password = unpad(cipher.decrypt(encrypted_password), AES.block_size).decode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_secret_answer = unpad(cipher.decrypt(encrypted_secret_answer), AES.block_size).decode('utf-8')
    except:
        decrypted_email = "undefined"
        decrypted_password = "undefined"
        decrypted_secret_answer = "undefined"

    email = decrypted_email
    password = decrypted_password
    secret_answer = decrypted_secret_answer
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

    if any(sql_injection_type in password for sql_injection_type in sql_injection_prevention):
        # If those SQL Injection strings are found, tell the API that an attempt was made and that it was blocked
        # by resetting the value to "0" or "invalid"
        print("SQL INJECTION ATTEMPT BLOCKED")
        print("Attempted input: " + password)
        password = "invalid"
        print("Value for password was reset to: " + password)

    if any(sql_injection_type in secret_answer for sql_injection_type in sql_injection_prevention):
        # If those SQL Injection strings are found, tell the API that an attempt was made and that it was blocked
        # by resetting the value to "0" or "invalid"
        print("SQL INJECTION ATTEMPT BLOCKED")
        print("Attempted input: " + secret_answer)
        secret_answer = "invalid"
        print("Value for secret answer was reset to: " + secret_answer)

    response = ""

    # Connect to database

    conn = sqlite3.connect('userdata_secure.db')

    # Create cursor

    eraseAccountData = conn.cursor()

    # Query the database

    try:
        # Retrieve the email and username where the email matches what the user entered
        eraseAccountData.execute(
            f'SELECT email, username, id FROM userdata WHERE email=\'{email}\' AND password =\'{password}\' AND secret_answer=\'{secret_answer}\'')
        rows = eraseAccountData.fetchall()

        if rows:
            for row in rows:
                username = str(row[1])
                id = str(row[2])
                print(id)

                loggedInUserID = str(row[2])
                eraseAccountData.execute(f'SELECT EXISTS (SELECT 1 FROM admin WHERE userdata_id = ?)', (loggedInUserID,))
                isUserAdmin = eraseAccountData.fetchone()[0]

                if isUserAdmin:
                    response = "It is not possible to erase an admin account"
                else:
                    eraseAccountData.execute(f'DELETE FROM userdata WHERE id=\'{id}\'')
                    print("Deleted user: ", username)
                    print("Deleted posts associated with user: ", username)
                    eraseAccountData.execute(f'DELETE FROM posts WHERE userdata_id=\'{id}\'')
                    response = "Successfully deleted account: " + username
            conn.commit()
        else:
            response = "No account with that email and/or password was found on the database"
    except:
        response = "Error with database"

    encrypted_data_b64, key_b64 = newGenerateKey(response)

    print(str(jsonify({"Token": encrypted_data_b64, "Key": key_b64})))

    return jsonify({"Token": encrypted_data_b64, "Key": key_b64})


# Re-route all of these when deploying to linux
# app.run(debug=True, host='10.0.2.5', port=8000) for example
if __name__ == '__main__':
    app.run(debug=True, host='10.0.2.5', port=9000)
