// Function to show the custom dialog
function showDialog(message) {
    const dialog = document.getElementById('customDialog');
    const dialogMessage = document.getElementById('dialogMessage');
    dialogMessage.textContent = message;
    dialog.classList.add('show');
}

// Function to close the custom dialog
function closeDialog() {
    const dialog = document.getElementById('customDialog');
    dialog.classList.remove('show');
}

// Close dialog when clicking outside
document.addEventListener('DOMContentLoaded', function() {
    // Handle dialog click outside
    const dialog = document.getElementById('customDialog');
    dialog.addEventListener('click', function(e) {
        if (e.target === dialog) {
            closeDialog();
        }
    });

    // Process messages on page load
    const messagesElement = document.getElementById('messages');
    const messagesData = messagesElement.getAttribute('data-messages');
    if (messagesData && messagesData.trim() !== '') {
        console.log('Messages found:', messagesData);
        const messages = messagesData.split('||');
        messages.forEach(function(message) {
            if (message.trim() !== '') {
                console.log('Showing message:', message);
                showDialog(message);
            }
        });
    }
});

// Handle escape key to close dialog
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeDialog();
    }
});
