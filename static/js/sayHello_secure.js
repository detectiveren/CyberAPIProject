async function sendName() {
    var txtName = document.getElementById("txtName");
    var name = txtName.value;

    // The secret key, it must be the exact same as the key on the Python Script
    var key = CryptoJS.enc.Utf8.parse('01234567890123456789012345678901');

    // Generate a random IV
    var iv = CryptoJS.lib.WordArray.random(16);

    try {
        // Encrypt the name using AES
        var encryptedName = CryptoJS.AES.encrypt(name, key, { iv: iv }).toString();
        // Re-route this to 'http://10.0.2.5:9000/secure-api/say-hi?name=' when deploying to linux
        // Make an asynchronous request to the API endpoint
        const response = await fetch('http://10.0.2.5:9000/secure-api/say-hi?name=' + encodeURIComponent(encryptedName) + '&iv=' + encodeURIComponent(iv.toString(CryptoJS.enc.Base64)), {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Check if the request was successful (status code 200)
        if (response.ok) {
            // Get the response JSON
            const data = await response.json();

            var jsonString = JSON.stringify(data); // Convert the JSON into string

            // Handle the response as needed
            // For example, you can display it in HTML
            var resultContainer = document.getElementById("resultContainer");
            resultContainer.innerHTML = jsonString;  // Return the JSON string
        } else {
            // Handle the case where the request was not successful
            console.error('Request failed with status:', response.status);
        }
    } catch (error) {
        // Handle any errors that occurred during the fetch
        console.error('Error during fetch:', error);
    }
}
