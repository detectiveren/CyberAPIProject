# Name: Eduardo Manuel Costa Moreira
# Student ID: MOR21500097
# Date: 17/01/2024

# Do not run independently, run this through main.py

# Current plan: Develop this communication app to send in the data inserted from the user and send the
# data to the API to output a desired outcome

# This is where imports are handled
import requests
import api_codes
import flask


def api_code_fetch(status_code):
    # Uses the status code it gets from the response and fetches the description of the status code
    status_response = str(status_code) + " " + api_codes.api_codes(status_code)
    return status_response


def API(url):
    response = requests.get(url)
    api_status = api_code_fetch(response.status_code)
    print("Status Code: " + api_status)
    data = response.text
    print(data)
