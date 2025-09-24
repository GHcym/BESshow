// Base JavaScript for BESshow

// Initialize dropdowns when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all Bootstrap dropdowns
    var dropdownElements = document.querySelectorAll('.dropdown-toggle');
    dropdownElements.forEach(function(dropdown) {
        new bootstrap.Dropdown(dropdown);
    });

    console.log('BESshow JavaScript initialized');
    console.log('Dropdowns initialized:', dropdownElements.length);
});