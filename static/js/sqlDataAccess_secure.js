async function sqlData() {
    function getRandomInteger(max) {
        return Math.floor(Math.random() * max);
    }


    var num = getRandomInteger(9)

    try {
        // Make an asynchronous request to the API endpoint
        // Re-route this to 'http://10.0.2.5:9000/unsecure-api/say-hi?name=' when deploying to linux
        const response = await fetch('http://127.0.0.1:9000/secure-api/grabSQLdata?sqlNumber=' + num, { method: 'get'});

        // Check if the request was successful (status code 200)
        if (response.ok) {
            // Get the response text
            const text = await response.text();

            // Display the response in your HTML page
            var resultContainer = document.getElementById("resultContainer");
            resultContainer.innerHTML = text;
        } else {
            // Handle the case where the request was not successful
            console.error('Request failed with status:', response.status);
        }
    } catch (error) {
        // Handle any errors that occurred during the fetch
        console.error('Error during fetch:', error);
    }
}