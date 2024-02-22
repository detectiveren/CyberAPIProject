# Name: Eduardo Manuel Costa Moreira
# Student ID: MOR21500097
# Date: 22/02/2024

# Here's where imports are handled
import requests
import communicate_with_unsecure_api
import communicate_with_secure_api
import decryptData

projectName = "Cyber API Security Project"
projectDesc = ("A Cyber-security API Project that will show the difference between \n"
               "an unsecure API and secure API (using encryption) to show how API Security is important \n"
               "in today's world")
projectCreator = "Eduardo Manuel Costa Moreira"
projectLatestUpdate = "22/02/2024"
milestoneNumber = "Milestone 11"

# API URLs
# REMINDER: Re-route all of these when deploying to linux
secure_api_local_say_hi = "http://127.0.0.1:8000/secure-api/say-hi?name="
unsecure_api_local_say_hi = "http://127.0.0.1:8000/unsecure-api/say-hi?name="
secure_api_local_predict_age = "http://127.0.0.1:8000/secure-api/age-prediction?name="
unsecure_api_local_predict_age = "http://127.0.0.1:8000/unsecure-api/age-prediction?name="
secure_api_local_email = "http://127.0.0.1:8000/secure-api/email?email="
unsecure_api_local_email = "http://127.0.0.1:8000/unsecure-api/email?email="
secure_api_test_sample_data = "http://127.0.0.1:8000/secure-api/sampleData?sampleDataNumber="
unsecure_api_test_sample_data = "http://127.0.0.1:8000/unsecure-api/sampleData?sampleDataNumber="


def welcomeMessage():  # This is the welcome message
    print("Welcome to my Final Year Project")
    print("Project Name: ", projectName, "\nProject Description: ", projectDesc)
    print("Project Creator: ", projectCreator)
    print("Project Latest Update: ", projectLatestUpdate)
    print(milestoneNumber)


def menu():
    user = ""
    welcomeMessage() # Display the welcome message
    print("1. Unsecure API")
    print("2. Secure API")
    print("3. Decrypt Data")
    print("4. Exit")
    while user != 4:
        user = int(input("Enter an API application to use (Type the number): "))

        if user == 1:
            print("NOTE: Ensure unsecure_api.py is running")
            print("Do you want a bunch of entry data or enter specific data")
            print("1. Predict Age by name")
            print("2. Say Hi to your name")
            print("3. Test Login")
            print("4. Test Sample Sensitive Data")
            user = int(input("Enter the type of Insecure API you want to use (Type the number): "))
            if user == 1:
                name = input("Enter a name and it will predict your age: ")
                communicate_with_unsecure_api.API(unsecure_api_local_predict_age + name)
            if user == 2:
                user = ""
                name = input("Enter a name and it will say hi: ")
                communicate_with_unsecure_api.API(unsecure_api_local_say_hi + name)
            if user == 3:
                user = ""
                email = input("Enter email to login: ")
                communicate_with_unsecure_api.API(unsecure_api_local_email + email)
            if user == 4:
                user = ""
                number = input("Enter a number between 1 to 15: ")
                communicate_with_unsecure_api.API(unsecure_api_test_sample_data + number)
        if user == 2:
            print("NOTE: Ensure secure_api.py is running")
            print("Do you want to Predict Age or have the API say Hi (more will be added later)")
            print("1. Predict Age by name")
            print("2. Say Hi to your name")
            print("3. Test Login")
            print("4. Test Sample Sensitive Data")
            user = int(input("Enter the type of Secure API you want to use (Type the number): "))
            if user == 1:
                name = input("Enter a name and it will predict your age: ")
                communicate_with_secure_api.API(secure_api_local_predict_age + name)
            if user == 2:
                user = ""
                name = input("Enter a name and it will say hi: ")
                communicate_with_secure_api.API(secure_api_local_say_hi + name)
            if user == 3:
                user = ""
                email = input("Enter email to login: ") # Email login at the moment, password will be added later
                communicate_with_secure_api.API(secure_api_local_email + email)
            if user == 4:
                user = ""
                number = input("Enter a number between 1 to 15: ")
                communicate_with_secure_api.API(secure_api_test_sample_data + number)

        if user == 3:
            print("Here you can decrypt the data from the secure API")
            user_key = input("Enter the key: ")
            user_token = input("Enter the token: ")
            local_response = decryptData.decryptData(user_key, user_token)
            print(local_response)



menu()
