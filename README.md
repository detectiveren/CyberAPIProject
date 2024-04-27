## Details on the APIs
insecure_api.py is the insecure API, this has to be ran independently (can be initiated from main.py)

secure_api.py is the secure API, this has to be ran independently (can be initiated from main.py)

main.py is where you launch into either insecure API or secure API, you will then have to navigate to either 127.0.0.1:8000 (insecure API) or 127.0.0.1:9000 (secure API) on the web

## API URLs/Endpoints

Insecure API URLs with functions so far:

http://127.0.0.1:8000/unsecure-api/age-prediction?name=(insert name here) predicts age based on name
http://127.0.0.1:8000/unsecure-api/say-hi?name=(insert name here) says hi to the user

Secure API URLs with functions so far: 

http://127.0.0.1:8000/secure-api/say-hi?name=(insert name here)
http://127.0.0.1:8000/secure-api/age-prediction?name=(insert name here)

## Running the API

IMPORTANT NOTE: When interacting with either the secure API or insecure API, ensure that the correct API is running in the background otherwise you'll recieve a 404 message or the page won't load

Steps to running and testing insecure API:

1) run insecure_api.py or run it through main.py (select option 1)
2) Go to the browser and enter 127.0.0.1:8000
3) Interact with the Insecure API pages listed on the home page (the secure API pages won't work as they are for the secure API)

Steps to running and testing secure API:

1) run secure_api.py or run it through main.py (select option 2)
2) Go to the browser and enter 127.0.0.1:9000
3) Interact with the Secure API pages listed on the home page (the insecure API pages won't work as they are for the insecure API)

## For Linux Testing

All learning materials used: 
https://www.zyte.com/blog/json-parsing-with-python/
https://anderfernandez.com/en/blog/how-to-create-api-python/

Run either insecure_api.py or secure_api.py in Ubuntu Server (ensure the host is 10.0.2.5)

Go to Kali Linux, open up Firefox (ensure all API URLs are routed to 10.0.2.5)

Type the URL of the API that you opened up in Ubuntu to test

Open up Wireshark to track traffic, display filter to "http"

On Firefox, interact with the API you have running

( WEB TESTING )

Ensure all the JS files have the response variable fetch URL changed to the host if you are using linux

For example in ```sampleSensitiveData_secure.js```, change the following ```const response = await fetch('http://127.0.0.1:9000/secure-api/sampleData?sampleDataNumber=' + num, { method: 'get'});``` to ```const response = await fetch('http://10.0.2.5:9000/secure-api/sampleData?sampleDataNumber=' + num, { method: 'get'});``` and for the insecure JS files, you do the same but change the port from 9000 to 8000

Also like the above, make sure both insecure_api.py and secure_api.py have the correct host in the code depending on the platform, the host is 10.0.2.5 for Ubuntu Server

Whether you are using Windows or Linux, to test the web versions of interactions between the client and API, go to http://127.0.0.1:8000/ (Insecure API) or http://127.0.0.1:9000/ (Secure API) if you are on Windows or http://10.0.2.5:8000/ (Insecure API) or http://10.0.2.5:9000/ (Secure API) if you are on Linux 

On the web page, interact with the API that is running

## Important Notes

Files that have been deprecated as they are no longer needed thanks to the project evolving

- communicate_with_secure_api.py is no longer needed as you can interact with the API on the web
- communicate_with_unsecure_api.py is no longer needed as you can interact with the API on the web
- decryptData.py is no longer needed as decryption is handled by both the JS files and the API scripts themselves

