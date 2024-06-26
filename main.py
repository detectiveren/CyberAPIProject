# Name: Eduardo Manuel Costa Moreira
# Student ID: MOR21500097
# Date: 27/04/2024

# Here's where imports are handled
import subprocess, api_config

projectName = "Cyber API Security Project"
projectDesc = ("A Cyber-security API Project that will show the difference between \n"
               "an insecure API and secure API (using encryption) to show how API Security is important \n"
               "in today's world")
projectCreator = "Eduardo Manuel Costa Moreira"
projectStudentID = "MOR21500097"
projectLatestUpdate = "27/04/2024"
milestoneNumber = "Milestone 14"


def welcomeMessage():  # This is the welcome message
    print("Welcome to my Final Year Project")
    print("Project Name: ", projectName, "\nProject Description: ", projectDesc)
    print("Student Name: ", projectCreator)
    print("Student ID: ", projectStudentID)
    print("Project Latest Update: ", projectLatestUpdate)
    print("Final Artefact Version\n" + milestoneNumber)


def menu():
    user = ""
    operatingSystem = api_config.configureAPI()
    os = api_config.setDeploymentSystem(operatingSystem)
    welcomeMessage()  # Display the welcome message
    print("1. Unsecure API")
    print("2. Secure API")
    print("3. Start both")
    print("4. Exit")
    while user != 4:
        user = int(input("Enter an API application to use (Type the number): "))
        if os == "Windows":
            if user == 1:
                subprocess.Popen(['python', 'insecure_api.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
            if user == 2:
                subprocess.Popen(['python', 'secure_api.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
            if user == 3:
                subprocess.Popen(['python', 'insecure_api.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
                subprocess.Popen(['python', 'secure_api.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        if os == "Linux":
            if user == 1:
                subprocess.Popen(['python3', 'insecure_api.py'])
            if user == 2:
                subprocess.Popen(['python3', 'secure_api.py'])
            if user == 3:
                subprocess.Popen(['python3', 'insecure_api.py'])
                subprocess.Popen(['python3', 'secure_api.py'])


menu()
