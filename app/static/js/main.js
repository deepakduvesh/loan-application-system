document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form[data-ajax="true"]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const action = form.getAttribute('action');
            const method = form.getAttribute('method') || 'POST';
            
            fetch(action, {
                method: method,
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.redirect) {
                    window.location.href = data.redirect;
                } else if (data.message) {
                    alert(data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
    
    
    const statusFilter = document.getElementById('statusFilter');
    if (statusFilter) {
        statusFilter.addEventListener('change', function() {
            const status = this.value;
            window.location.href = `/applications?status=${status}`;
        });
    }
});

document.getElementById('decisionForm').addEventListener('submit', function(e) {
    e.preventDefault();

    fetch(this.action, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            status: document.getElementById('status').value,
            officer_notes: document.getElementById('officerNotes').value
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message); 
            window.location.reload(); 
        }
    })
    .catch(error => console.error('Error:', error));
});