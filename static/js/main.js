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
    const dialog = document.getElementById('customDialog');
    dialog.addEventListener('click', function(e) {
        if (e.target === dialog) {
            closeDialog();
        }
    });
});

// Handle escape key to close dialog
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeDialog();
    }
});
