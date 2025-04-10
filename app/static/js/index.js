
// Variable for tether text input
let tether;

// Constant for tether-submit button
const tetherSubmitBtn = document.getElementById("tether-submit");
// Variables for tether-text and tether-result
let tetherText = document.getElementById("tether-text");
let tetherResult = document.getElementById("tether-result");

tetherSubmitBtn.onclick = () => {
    // Get tether text from input using element id
    tether = document.getElementById("tether-text").value;
    // Now want to display said text instead of input box
    document.getElementById("tether-result").textContent = tether;
    // And hide the input text box and submit button
    tetherText.classList.add("hidden");
    tetherSubmitBtn.classList.add("hidden");
}

tetherResult.onclick = () => {
    tetherResult.classList.remove("hidden");
    tetherText.classList.remove("hidden");
    tetherSubmitBtn.classList.remove("hidden");
}

// Function that activates when checkbox for anchor habits are checked, indicating completion
// Function will then use fetch() to trigger POST to tell Flask to update DB
function markHabitComplete(taskId) {
    // Fetch sends a request to flask server
    // POSTing to a dynamic URL like /complete_habit/7
    // Translation: "Hey, mark habit 7 as complete"
    fetch(`/complete_habit/${taskId}`, { 
        // Request config
        // Making a POST request | Set Content-Type to application/json even if 
        // we're not sending a body (good habit)
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        }
        // BODY
    })
    // Waits for Flask's response
    // .json() converts it from a raw response to usable JS object ( {success: true} )
    .then(response => response.json())
    // Once you have that response, do something - here, just log it
    // Later, could update the UI, disable the checkbox, add animation, etc
    .then(data => {
        console.log('Habit marked complete:', data);
        // Optional, update UI here later
    })
    // Error Catching
    // If network fails or Flask throws an error, you'll see it here
    // Could later show a popup, retry, etc.
    .catch(error => {
        console.error('Error marking habit complete:', error)
    });
}