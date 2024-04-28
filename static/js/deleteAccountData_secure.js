async function deleteData() {
    var txtName = document.getElementById("txtName");
    var txtName2 = document.getElementById("txtName2");
    var email = txtName.value;
    var password = txtName2.value;

    // The secret key, it must be the exact same as the key on the Python Script
    var key = CryptoJS.enc.Utf8.parse('01234567890123456789012345678901');

    // Generate a random IV
    var iv = CryptoJS.lib.WordArray.random(16);

    try {
        var encryptedEmail = CryptoJS.AES.encrypt(email, key, { iv: iv }).toString();
        var encryptedPassword = CryptoJS.AES.encrypt(password, key, { iv: iv }).toString();
        // Make an asynchronous request to the API endpoint
        // Re-route this to 'http://10.0.2.5:9000/secure-api/eraseDataPortal?e=' when deploying to linux
        const response = await fetch('http://10.0.2.5:9000/secure-api/eraseDataPortal?e=' + encodeURIComponent(encryptedEmail) + '&p=' + encodeURIComponent(encryptedPassword) + '&iv=' + encodeURIComponent(iv.toString(CryptoJS.enc.Base64)), {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Check if the request was successful (status code 200)
        if (response.ok) {
            // Get the response text
            const data = await response.json();

            var jsonString = JSON.stringify(data); // Convert the JSON into string

            // Display the response in your HTML page
            var resultContainer = document.getElementById("resultContainer");
            resultContainer.innerHTML = jsonString;
        } else {
            // Handle the case where the request was not successful
            console.error('Request failed with status:', response.status);
        }
    } catch (error) {
        // Handle any errors that occurred during the fetch
        console.error('Error during fetch:', error);
    }
}