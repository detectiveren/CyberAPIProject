communicate_with_insecure_api.py is the python script to communicate with the unsecure API and use its functions (cannot be ran independently, launch main.py)

insecure_api.py is the API itself, this has to be ran independently (cannot be initiated from main.py)

communicate_with_secure_api.py is the python script to communicate with the secure API and use its functions, it can decrypt any data recieved (cannot be ran independently, launch main.py)

secure_api.py is the API itself, this has to be ran independently (cannot be initiated from main.py)

main.py is where you launch into either communicated with unsecure API or secure API, you will have a list of choices on functions to use.

Unsecure API URLs with functions so far:

http://127.0.0.1:8000/unsecure-api/age-prediction?name=(insert name here) predicts age based on name
http://127.0.0.1:8000/unsecure-api/say-hi?name=(insert name here) says hi to the user

Secure API URLs with functions so far: 

http://127.0.0.1:8000/secure-api/say-hi?name=(insert name here)
http://127.0.0.1:8000/secure-api/age-prediction?name=(insert name here)

IMPORTANT NOTE: When communicating with either the secure API or unsecure API, ensure that the correct API is running in the background otherwise you'll recieve a 404 Message 

Steps to running and testing unsecure API:

1) run insecure_api.py
2) run main.py
3) Type "1" when asked "Enter an API application to use (Type the number): "
4) you can also run the API URLs above for the unsecure API on the web

Steps to running and testing secure API:

1) run secure_api.py
2) run main.py
3) Type "2" when asked "Enter an API application to use (Type the number): "
4) To decrypt the data, when entering the key make sure it's everything within b'key here' and when entering the token make sure its everything within b'token here'
5) you can also run the API URLs above for the unsecure API on the web

All learning materials used: 
https://www.zyte.com/blog/json-parsing-with-python/
https://anderfernandez.com/en/blog/how-to-create-api-python/

( FOR LINUX TESTING )

Run either insecure_api.py or secure_api.py in Ubuntu Server (ensure the host is 10.0.2.5)

Go to Kali Linux, open up main.py (ensure all API URLs are routed to 10.0.2.5)

Select the API that you opened up in Ubuntu to test

Open up Wireshark to track traffic, display filter to "http"

On main.py, interact with the API you have selected 

( WEB TESTING )

Ensure all the JS files have the response variable fetch URL changed to the host if you are using linux

For example in ```sampleSensitiveData_secure.js```, change the following ```const response = await fetch('http://127.0.0.1:8000/secure-api/sampleData?sampleDataNumber=' + num, { method: 'get'});``` to ```const response = await fetch('http://10.0.2.5:8000/secure-api/sampleData?sampleDataNumber=' + num, { method: 'get'});```

Also like the above, make sure both insecure_api.py and secure_api.py have the correct host in the code depending on the platform, the host is 10.0.2.5 for Ubuntu Server

Whether you are using Windows or Linux, to test the web versions of interactions between the client and API, go to http://127.0.0.1:8000/ if you are on Windows or http://10.0.2.5:8000/ if you are on Linux 

On the web page, interact with the API that is running

( IMPORTANT NOTES )

communicate_with_secure_api.py no longer works at the moment as it used to use Fernet to decrypt the encrypted data however Fernet is no longer being used in this project, instead the data is encrypted in AES (Advanced Encryption Standard) and the python script will be changed to support that soon

decryptData.py no longer works for the same reason
