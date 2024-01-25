async function sendName() {
    var txtName = document.getElementById("txtName");
    var name = txtName.value;

    try {
        // Make an asynchronous request to the API endpoint
        // Re-route this to 'http://10.0.2.4:8000/unsecure-api/age-prediction?name=' when deploying to linux
        const response = await fetch('http://127.0.0.1:8000/unsecure-api/age-prediction?name=' + name, { method: 'get'});

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