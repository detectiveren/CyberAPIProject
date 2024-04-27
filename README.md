## Details on the APIs
insecure_api.py is the insecure API, this has to be ran independently (can be initiated from main.py)

secure_api.py is the secure API, this has to be ran independently (can be initiated from main.py)

main.py is where you launch into either insecure API or secure API, you will then have to navigate to either 127.0.0.1:8000 (insecure API) or 127.0.0.1:9000 (secure API) on the web

## API URLs/Endpoints

Insecure API URLs that can be interacted with so far:

### Windows
- http://127.0.0.1:8000/insecure/sayhello ```Says Hello to the User```

- http://127.0.0.1:8000/insecure/ageprediction ```Predicts the user's age based on their name```

- http://127.0.0.1:8000/insecure/email ```Users logs in through the API using their email (uses API's database)```

- http://127.0.0.1:8000/insecure/sampleSensitiveData ```Sample sensitive data from a textfile on the API's directory```

- http://127.0.0.1:8000/insecure/sqlData ```Sample user data on the API's database```

- http://127.0.0.1:8000/insecure/sqlUserPosts ```Sample user posts on the API's database```

### Linux
- http://10.0.2.5:8000/insecure/sayhello 

- http://10.0.2.5:8000/insecure/ageprediction 

- http://10.0.2.5:8000/insecure/email 

- http://10.0.2.5:8000/insecure/sampleSensitiveData 

- http://10.0.2.5:8000/insecure/sqlData 

- http://10.0.2.5:8000/insecure/sqlUserPosts 


Secure API URLs that can be interacted with so far: 

### Windows
- http://127.0.0.1:9000/secure/sayhello ```Says Hello to the User```

- http://127.0.0.1:9000/secure/ageprediction ```Predicts the user's age based on their name```

- http://127.0.0.1:9000/secure/email ```Users logs in through the API using their email (uses API's database)```

- http://127.0.0.1:9000/secure/sampleSensitiveData ```Sample sensitive data from a textfile on the API's directory```

- http://127.0.0.1:9000/secure/sqlData ```Sample user data on the API's database```

- http://127.0.0.1:9000/secure/sqlUserPosts ```Sample user posts on the API's database```

### Linux
- http://10.0.2.5:8000/secure/sayhello 

- http://10.0.2.5:8000/secure/ageprediction 

- http://10.0.2.5:8000/secure/email 

- http://10.0.2.5:8000/secure/sampleSensitiveData 

- http://10.0.2.5:8000/secure/sqlData 

- http://10.0.2.5:8000/secure/sqlUserPosts 

## Running the API

IMPORTANT NOTE: When interacting with either the secure API or insecure API, ensure that the correct API is running in the background otherwise you'll recieve a 404 message or the page won't load

Steps for running and testing insecure API:

1) run insecure_api.py or run it through main.py (select option 1)
2) Go to the browser and enter 127.0.0.1:8000
3) Interact with the Insecure API pages listed on the home page (the secure API pages won't work as they are for the secure API)

Steps for running and testing secure API:

1) run secure_api.py or run it through main.py (select option 2)
2) Go to the browser and enter 127.0.0.1:9000
3) Interact with the Secure API pages listed on the home page (the insecure API pages won't work as they are for the insecure API)

## For Linux Testing

### VM Account Info for Ubuntu Server

- username: eddy
- password: 123

### VM Account Info for Kali Linux

- username: kali
- password: kali

### Setting up the API on Linux

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

Git cloning the private GitHub repository containing the project code into Linux can be done using GitHub tokens, this token is set to never expire (which is usually not recommended but for the sake of making this project easier for deployment it won't expire) 


The command to git clone the private repo is as follows: 

sudo git clone ```https://ghp_ttzfYfnv1CQqdM7ok2GhwNQ9u15UAB1la5yA@github.com/detectiveren/CyberAPIProject.git```


Once git cloned, before running everything, make sure the response variable in all the JS files point towards the host of the Ubuntu Server which is 10.0.2.5 and ensure that both unsecure_api.py and secure_api.py are pointing towards the host too


Same applies for main.py if you want to run the APIs through there

