
/* -------------- NEW RETREAT FORM JS ------------------------------- */

document.getElementById('newRetreat').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData(this); // Create FormData object from the form
    const postFlaskUrl = "{{ admin_panel.submit_new_retreat }}"

    fetch(postFlaskUrl, { // Replace '/submit_form' with your Flask route
        method: 'POST',
        body: formData
    })
    .then(response => response.json()) // Assuming your Flask backend returns JSON
    .then(data => {
        console.log('Success:', data);
        // Handle success response (e.g., display a message)
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle errors
    });
});