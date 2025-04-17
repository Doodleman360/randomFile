// Function to confirm file deletion
function confirmDelete(filePath) {
    document.getElementById('deleteFilePath').value = filePath;
    document.getElementById('deleteFileName').textContent = filePath.split('\\').pop();
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    deleteModal.show();
}

// Function to show move file modal
function showMoveModal(filePath) {
    document.getElementById('moveFilePath').value = filePath;
    document.getElementById('moveFileName').textContent = filePath.split('\\').pop();

    // Fetch directories for the dropdown
    fetch('{{ url_for("main.get_directories") }}')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('destination');
            select.innerHTML = '';

            // Add a root directory option
            const rootOption = document.createElement('option');
            rootOption.value = '';
            rootOption.textContent = 'Root Directory';
            select.appendChild(rootOption);

            // Add all directories
            data.directories.forEach(dir => {
                const option = document.createElement('option');
                option.value = dir;
                option.textContent = dir;
                select.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching directories:', error);
        });

    const moveModal = new bootstrap.Modal(document.getElementById('moveModal'));
    moveModal.show();
}

// Tree view functionality
document.addEventListener('DOMContentLoaded', function () {
    // Handle tree item clicks
    document.querySelectorAll('.tree-item-content').forEach(item => {
        item.addEventListener('click', function (e) {
            const path = this.getAttribute('data-path');
            const type = this.getAttribute('data-type');
            const toggle = this.querySelector('.tree-toggle');

            // If clicking on the toggle button or if it's a directory
            if (e.target === toggle || (type === 'directory' && toggle.textContent === '+' || toggle.textContent === '-')) {
                // Toggle the children's visibility
                const children = this.nextElementSibling;
                if (children && children.classList.contains('tree-children')) {
                    children.classList.toggle('show');
                    toggle.textContent = children.classList.contains('show') ? '-' : '+';
                }
                e.stopPropagation(); // Prevent navigation
            }
        });
    });

    // Auto-dismiss flash messages after 5 seconds
    setTimeout(function () {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});