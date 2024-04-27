# Name: Eduardo Manuel Costa Moreira
# Student ID: MOR21500097
# Date: 22/02/2024

# Here's where imports are handled
import subprocess

projectName = "Cyber API Security Project"
projectDesc = ("A Cyber-security API Project that will show the difference between \n"
               "an unsecure API and secure API (using encryption) to show how API Security is important \n"
               "in today's world")
projectCreator = "Eduardo Manuel Costa Moreira"
projectLatestUpdate = "27/04/2024"
milestoneNumber = "Milestone 14"

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
    print("3. Start both")
    print("4. Exit")
    while user != 4:
        user = int(input("Enter an API application to use (Type the number): "))

        if user == 1:
            subprocess.Popen(['python', 'unsecure_api.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        if user == 2:
            subprocess.Popen(['python', 'secure_api.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        if user == 3:
            subprocess.Popen(['python', 'unsecure_api.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
            subprocess.Popen(['python', 'secure_api.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)



menu()
