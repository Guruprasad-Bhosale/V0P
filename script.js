// Hide the loader when the page content is loaded
window.onload = function () {
    const loader = document.querySelector('.loader');
    const header = document.querySelector('header');
    const main = document.querySelector('main');

    // Hide the loader and show the main content
    if (loader) {
        loader.style.display = 'none';  // Hide the loader
    }

    if (header && main) {
        header.style.display = 'block'; // Show the header
        main.style.display = 'block';   // Show the main content
    }
};

// Handle form submission for plant image upload
document.getElementById('uploadForm').onsubmit = async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById('plantImage');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.plant) {
            // Display plant info
            document.getElementById('plantName').innerText = result.plant;
            document.getElementById('plantInfo').innerText = result.info;
        } else {
            // Display error message
            document.getElementById('errorMessage').innerText = result.error;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('errorMessage').innerText = 'An error occurred';
    }
};
