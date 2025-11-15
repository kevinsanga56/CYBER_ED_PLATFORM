function checkUrl() {
    const url = document.getElementById('url_input').value;
    const feedbackDiv = document.getElementById('url_feedback');
    const checkButton = document.getElementById('check_button');

    // 1. Input Validation
    if (url.length === 0) {
        feedbackDiv.innerHTML = '<p class="warning-text">Please enter a link to check.</p>';
        return;
    }
    
    // Disable button during check
    checkButton.disabled = true;
    checkButton.textContent = 'Checking...';
    feedbackDiv.innerHTML = '<p>Processing...</p>'; // Show processing message

    // 2. AJAX Request to Flask Back-end
    fetch('/check_url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'url': url })
    })
    .then(response => {
        // Check if the response was successful (HTTP status 200)
        if (!response.ok) {
            throw new Error(`Server returned status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // 3. Handle Data and Update HTML
        checkButton.disabled = false;
        checkButton.textContent = 'Check Link Safety';
        
        let resultClass;
        let statusText = data.status || 'Error';
        let messageText = data.message || 'No detailed message provided.';

        // Map status to CSS classes
        if (statusText === 'Safe') {
            resultClass = 'result-safe';
        } else if (statusText === 'Warning' || statusText === 'Danger') {
            resultClass = 'result-fail'; 
        } else {
            // Handle the "error" status from app.py
            resultClass = 'warning-text';
        }

        feedbackDiv.innerHTML = `
            <div class="${resultClass}" style="padding: 15px;">
                <strong>Status: ${statusText}</strong>
                <p>${messageText}</p>
            </div>
        `;
    })
    .catch((error) => {
        // 4. Handle Network or Parsing Errors
        checkButton.disabled = false;
        checkButton.textContent = 'Check Link Safety';
        feedbackDiv.innerHTML = `<p class="warning-text">Error communicating with server: ${error.message}</p>`;
        console.error('Error:', error);
    });
}