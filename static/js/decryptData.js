// decryptScript.js

// Function to decrypt AES-encrypted data and sanitize the result
function decryptAndSanitizeAES(encryptedData, key) {
    // Decrypt the data using AES
    const decryptedDataWordArray = CryptoJS.AES.decrypt({ ciphertext: CryptoJS.enc.Base64.parse(encryptedData) }, CryptoJS.enc.Base64.parse(key), {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });

    // Convert the decrypted WordArray to a string and sanitize it
    const decryptedDataString = decryptedDataWordArray.toString(CryptoJS.enc.Utf8);
    const sanitizedDecryptedData = decryptedDataString.replace(/[^\x20-\x7E]/g, ''); // Remove non-printable characters

    return sanitizedDecryptedData;
}

// Helper function to convert base64 string to Uint8Array
function base64ToArrayBuffer(base64String) {
    // Decode the base64 string
    const binaryString = window.atob(base64String);
    const uint8Array = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
        uint8Array[i] = binaryString.charCodeAt(i);
    }
    return uint8Array.buffer;
}

// Add event listener to the Decrypt Message button
document.getElementById("decryptButton").addEventListener("click", function() {
    // Get the content of the resultContainer div
    const resultContainerContent = document.getElementById("resultContainer").innerText.trim();

    // Parse the content as JSON
    const result = JSON.parse(resultContainerContent);

    // Get the encrypted message (Token) and key from the parsed JSON
    const encryptedData = result.Token;
    const key = result.Key;

    // Decrypt the message
    const decryptedMessage = decryptAndSanitizeAES(encryptedData, key);

    // Display the decrypted message
    document.getElementById("decryptedMessage").innerText = decryptedMessage;
});