# Name: Eduardo Manuel Costa Moreira
# Student ID: MOR21500097
# Date: 17/01/2024

def api_codes(code):
    if code == 200:
        response = "Everything went okay and a result has been returned"
    elif code == 301:
        response = "The server is redirecting you to a different endpoint"
    elif code == 400:
        response = "The server thinks you made a bad request"
    elif code == 401:
        response = "The server thinks you are not authenticated"
    elif code == 403:
        response = "The resource you're trying to access is forbidden"
    elif code == 404:
        response = "Not found"
    elif code == 503:
        response = "The server is not ready to handle your request"

    return response