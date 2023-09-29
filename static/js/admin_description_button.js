// admin_description_button.js

document.addEventListener('DOMContentLoaded', function() {
    const toggleButtons = document.querySelectorAll('.toggle-description');

    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const descriptionContent = this.nextElementSibling;

            if (descriptionContent.classList.contains('hidden-description')) {
                descriptionContent.classList.remove('hidden-description');
                this.textContent = 'Свернуть';
            } else {
                descriptionContent.classList.add('hidden-description');
                this.textContent = 'Развернуть';
            }
        });
    });
});