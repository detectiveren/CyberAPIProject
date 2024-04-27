# Name: Eduardo Manuel Costa Moreira
# Student ID: MOR21500097
# Date: 27/04/2024


import os
import sys
import re


# This just changes the IP addresses to match the OS it is on

def editFiles(directory, ip_address):
    # Iterate over all files in the directory
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # Check if the file is a Python, JS or HTML file
            if file_name.endswith('.py'):
                editPyFile(file_path, ip_address)
            elif file_name.endswith('.js'):
                editJSFile(file_path, ip_address)
            elif file_name == 'index.html':
                editHTMLFile(file_path, ip_address)


def editPyFile(file_path, ip_address):
    # Check if the Python file exists and is readable
    if os.path.exists(file_path) and os.access(file_path, os.R_OK):
        # Read the file line by line and edit the lines containing the ip address
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        with open(file_path, 'w', encoding='utf-8') as file:
            for line in lines:
                if 'app.run(debug=True, host=' in line:
                    # Replace the IP address based on the user's choice
                    line = re.sub(r"host='(?:10\.0\.2\.5|127\.0\.0\.1)'", f"host='{ip_address}'", line)
                file.write(line)


def editJSFile(file_path, ip_address):
    # Check if the JS file exists and is readable
    if os.path.exists(file_path) and os.access(file_path, os.R_OK):
        # Read the file line by line and edit the lines containing the ip address
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        with open(file_path, 'w', encoding='utf-8') as file:
            for line in lines:
                if "const response = await fetch('http://" in line:
                    # Replace the IP address
                    line = re.sub(r"http://(?:10\.0\.2\.5|127\.0\.0\.1):", f"http://{ip_address}:", line)
                file.write(line)


def editHTMLFile(file_path, ip_address):
    # Check if the html file exists and is readable
    if os.path.exists(file_path) and os.access(file_path, os.R_OK):
        # Read the file content only if it's index.html
        if os.path.basename(file_path) == 'index.html':
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Replace the IP address in the html file
            content = re.sub(r"http://(?:10\.0\.2\.5|127\.0\.0\.1):", f"http://{ip_address}:", content)

            # Write the changes
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)


def configureAPI():
    # Ask the user what operating system they are on
    os_choice = input("Enter your operating system choice (Windows/Linux): ").lower()
    if os_choice not in ['windows', 'linux']:
        print("Invalid choice. Please enter 'Windows' or 'Linux'.")
        sys.exit(1)

    # Set the IP address based on the user's choice
    if os_choice == 'windows':
        ip_address = '127.0.0.1'
    else:
        ip_address = '10.0.2.5'

    # Ask the user for the directory to scan
    directory = "."

    editFiles(directory, ip_address)
