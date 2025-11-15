// Function to update the visual strength meter based on the score (0-4)
function updateMeter(score, feedback) {
    const levelElement = document.getElementById('strength_level');
    const feedbackElement = document.getElementById('strength_feedback');
    
    // Define the style properties based on the score
    let width = (score / 4) * 100; // Calculate width percentage
    let color = '';

    if (score <= 1) {
        color = 'var(--color-red)'; // Use red for weak
    } else if (score === 2) {
        color = 'var(--color-orange)'; // Orange for moderate
    } else if (score === 3) {
        color = 'var(--color-yellow)'; // Yellow for good
    } else if (score === 4) {
        color = 'var(--color-green)'; // Green for excellent
    }

    // Apply styles and update feedback text
    levelElement.style.width = width + '%';
    levelElement.style.backgroundColor = color;
    feedbackElement.innerHTML = `**Strength Score: ${score}/4**<br>${feedback}`;
}

// Main function called every time the user types a key
function checkStrength() {
    const password = document.getElementById('password_input').value;

    if (password.length === 0) {
        updateMeter(0, "Start typing to see feedback!");
        return;
    }

    // Use the Fetch API to send the password to the Flask back-end
    fetch('/check_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        // Send the password as a JSON object
        body: JSON.stringify({ 'password': password })
    })
    .then(response => response.json()) // Get the JSON response from Flask
    .then(data => {
        // Update the meter and feedback based on the data received
        updateMeter(data.score, data.feedback);
    })
    .catch((error) => {
        console.error('Error:', error);
        updateMeter(0, "An error occurred while checking strength.");
    });
}