// Main JavaScript file

// Handle form submissions
document.addEventListener('DOMContentLoaded', function() {
    // Event Registration
    const eventForms = document.querySelectorAll('.event-registration-form');
    eventForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const eventId = form.dataset.eventId;
            try {
                const response = await fetch(`/api/events/${eventId}/register/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                });
                if (response.ok) {
                    showAlert('Successfully registered for the event!', 'success');
                    updateEventCapacity(eventId);
                } else {
                    showAlert('Failed to register for the event.', 'danger');
                }
            } catch (error) {
                console.error('Error:', error);
                showAlert('An error occurred.', 'danger');
            }
        });
    });

    // TimeBank Offer/Need Form
    const timebankForm = document.getElementById('timebank-form');
    if (timebankForm) {
        timebankForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(timebankForm);
            try {
                const response = await fetch('/api/timebank/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify(Object.fromEntries(formData))
                });
                if (response.ok) {
                    showAlert('Successfully posted to TimeBank!', 'success');
                    timebankForm.reset();
                } else {
                    showAlert('Failed to post to TimeBank.', 'danger');
                }
            } catch (error) {
                console.error('Error:', error);
                showAlert('An error occurred.', 'danger');
            }
        });
    }
});

// Utility Functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.querySelector('main').insertBefore(alertDiv, document.querySelector('main').firstChild);
    setTimeout(() => alertDiv.remove(), 5000);
}

function updateEventCapacity(eventId) {
    const capacityElement = document.querySelector(`#event-${eventId} .capacity`);
    if (capacityElement) {
        let capacity = parseInt(capacityElement.textContent);
        capacityElement.textContent = capacity - 1;
    }
} 