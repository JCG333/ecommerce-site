
// ===================== UNIVERSAL ========================

// ================ logo redirect =================

function logo_redirect() {
    window.location.href = '/';
}
// event lisenter for logo redirect
document.getElementById('logo').addEventListener('click', function () {
    logo_redirect();
});

// ===================== cart redirect ========================
function cart_redirect() {
    fetch('/login_status')
        // check if response is OK
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => Promise.reject(error));
            }
            return response.json();
        })
        // if OK
        .then(data => {
            window.location.href = '/cart';
        })
        // Error handling
        .catch(error => {
            showError(error.message, false);
        });
}
// event lisenter for logo redirect
document.getElementById('cart').addEventListener('click', function () {
    cart_redirect();
});

// ===================== account redirect ========================
function account_redirect() {
    fetch('/login_status')
        // check if response is OK
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => Promise.reject(error));
            }
            return response.json();
        })
        // if OK
        .then(data => {
            window.location.href = '/myaccount';
        })
        // Error handling
        .catch(error => {
            showError(error.message, false);
        });
}


// event lisenter for logo redirect
document.getElementById('account-link').addEventListener('click', function () {
    account_redirect();
});

// =================== register redirect ===================

function register_redirect() {
    window.location.href = '/register';
}
// event lisenter for logo redirect
document.getElementById('register_button').addEventListener('click', function () {
    register_redirect();
});

// =================== logout ===================
function logout_redirect() {
    fetch('/logout')
        // check if response is OK
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => Promise.reject(error));
            }
            return response.json();
        })
        // if OK
        .then(data => {
            showError('User logged out successfully!', true);
            document.getElementById('user-name').textContent = '';
            updateCartNotification();
            admin_button_status();
        })
        // Error handling
        .catch(error => {
            showError(error.message, false);
        });
}
// event lisenter for logo redirect
document.getElementById('logout-link').addEventListener('click', function () {
    logout_redirect();
});

// ===================== login form LOGIN ========================

function login(email, password) {
    fetch(`/login`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
        // check if response is OK
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => Promise.reject(error));
            }
            return response.json();
        })
        // if OK
        .then(data => {
            showError('User logged in successfully!', true);
            document.getElementById('user-name').textContent = data.username; // Display the user's name
            updateCartNotification();
            admin_button_status();
        })
        // Error handling
        .catch(error => {
            showError(error.message, false);
        });
}

// event lisenter for login button
document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the form from being submitted normally
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    login(email, password);
});

// =================== login form functionality =====================

// Add a click event listener to the account icon
document.getElementById('account-icon').addEventListener('click', function (event) {
    var dropdownContent = document.getElementById('loginDropdown');
    if (dropdownContent.style.display === "none") {
        dropdownContent.style.display = "block";
    } else {
        dropdownContent.style.display = "none";
    }
    event.stopPropagation();
});
// Close the dropdown if the user clicks outside of it
window.addEventListener('click', function () {
    var dropdownContent = document.getElementById('loginDropdown');
    dropdownContent.style.display = "none"; // Hide the dropdown when anywhere else on the window is clicked
});
// Prevent clicks inside the dropdown from closing the dropdown
document.getElementById('loginForm').addEventListener('click', function (event) {
    event.stopPropagation(); // Stop the click event from bubbling up to parent elements
});

// =================== categories =====================

function redirect_categories(category_name) {
    window.location.href = '/categories/' + category_name;
}

categoriesList.addEventListener('click', function (event) {
    event.preventDefault();
    var target = event.target;
    if (target.tagName === 'A') {
        redirect_categories(target.textContent);
    }
});


//==================== search bar ==================

//search bar
function search(event) {
    if (event.key === 'Enter') {
        var searchQuery = document.getElementById('search').value;
        window.location.href = '/search/' + searchQuery;
    }
}
// event listener for search bar
document.getElementById('search').addEventListener('keypress', search);

// =================== cart notification =====================
function updateCartNotification() {
    fetch('/order_size')
        // check if response is OK
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => Promise.reject(error));
            }
            return response.json();
        })
        // if OK
        .then(data => {
            if (data.LoggedIn == false) {
                console.log('not logged in');
                document.getElementById('round-div').textContent = 0;
            } else {
                if (data.order_size > 0) {
                    document.getElementById('round-div').textContent = data.order_size;
                } else {
                    document.getElementById('round-div').textContent = 0;
                }
            }
        })
        // Error handling
        .catch(error => {
            console.log('Error fetching order size: ' + error);
        });
}

// =================== admin button =====================
function admin_button_status() {
    fetch('/get_user_role')
        .then(response => response.json())
        .then(data => {
            if (data.role === true) {
                console.log('admin');
                document.getElementById('console-button').style.display = 'block';
            }
            else {
                console.log('not admin');
                document.getElementById('console-button').style.display = 'none';
            }
        });
}
// event listener for admin button
document.getElementById('console-button').addEventListener('click', function () {
    window.location.href = '/admin_console';
});

/*----- error message -----*/
function showError(message, status_code) {
    var errorMessage = document.getElementById('error-message');
    if (!status_code) {
        errorMessage.innerHTML = '<p>Error: ' + message + '</p>';
        errorMessage.classList.remove('sucess-message');
        errorMessage.classList.add('error-message');
        errorMessage.style.display = 'block'; // Show the error message
    } else {
        errorMessage.innerHTML = '<p>Success: ' + message + '</p>';
        errorMessage.classList.remove('error-message');
        errorMessage.classList.add('success-message');
        errorMessage.style.display = 'block'; // Show the success message
    }
    // Hide the error message after 5 seconds
    setTimeout(function () {
        errorMessage.style.display = 'none';
    }, 5000);
}


// =================== admin bar functionality =====================
document.addEventListener('DOMContentLoaded', function () {
    // Hide all content sections except the placeholder section
    const contentSections = document.querySelectorAll('.content-section');
    contentSections.forEach(section => {
        section.style.display = 'none';
    });

    // Show the placeholder section
    const placeholderSection = document.getElementById('placeholder-section');
    if (placeholderSection) {
        placeholderSection.style.display = 'block';
    }
});

function toggleSection(sectionId) {
    // Hide all content sections
    const contentSections = document.querySelectorAll('.content-section');
    contentSections.forEach(section => {
        section.style.display = 'none';
    });

    // Show the selected content section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.style.display = 'block';
    }
}

window.onload = function () {
    fetch('/get_username')
        .then(response => response.json())
        .then(data => {
            if (data.username) {
                document.getElementById('user-name').textContent = data.username; // Display the user's name
            }
            else {
                document.getElementById('user-name').textContent = ''; // Display nothing
            }
        });
    // Call the function when the page loads
    updateCartNotification();
    admin_button_status();

};

// Add to stock
document.querySelectorAll('.plus-button').forEach(function(button) {
    button.addEventListener('click', function() {
        var productId = this.getAttribute('data-product-id');
        var quantityElement = this.parentElement.parentElement.querySelector('td:nth-child(3)'); // Get the quantity element
        fetch('/update_quantity', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({product_id: productId, change: 1}),
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            // Update the quantity on the page
            var currentQuantity = parseInt(quantityElement.textContent);
            quantityElement.textContent = currentQuantity + 1;
        });
    });
});

// Remove from stock
document.querySelectorAll('.minus-button').forEach(function(button) {
    button.addEventListener('click', function() {
        var productId = this.getAttribute('data-product-id');
        var quantityElement = this.parentElement.parentElement.querySelector('td:nth-child(3)'); // Get the quantity element
        fetch('/update_quantity', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({product_id: productId, change: -1}),
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            // Update the quantity on the page
            var currentQuantity = parseInt(quantityElement.textContent);
            if (currentQuantity > 0) { // Ensure quantity doesn't go below 0
                quantityElement.textContent = currentQuantity - 1;
            }
        });
    });
});

// Delete product
document.querySelectorAll('.delete-button').forEach(button => {
    
    button.addEventListener('click', function() {
        const productId = this.dataset.productId;
        fetch(`/delete_product/${productId}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove the product row from the table
                const parentElement = this.parentElement.parentElement.parentElement;

                // Remove the parent element
                parentElement.remove();
                
            } else {
                // Show an error message
                console.error('Error:', data.error);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});


// Create new product
document.getElementById('create_product_form').addEventListener('submit', function(event) {
    // Prevent the form from submitting normally
    event.preventDefault();

    // Create a FormData object from the form
    const formData = new FormData(this);

    // Send the form data to the server
    fetch('/create_product', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Handle the JSON response
        if (data.success) {
            // Clear the form
            document.getElementById('create_product_form').reset();

            // Optionally, reload the page to update the product list
            location.reload();
        } else {
            // Show an error message
            console.error('Error:', data.error);
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        // Handle non-JSON responses here, e.g., display an error message to the user
    });
});


// New price
document.querySelectorAll('.update-price-button').forEach(button => {
    button.addEventListener('click', function() {
        const productId = this.dataset.productId;
        const inputElement = this.parentElement.querySelector('.new-price-input');
        const newPrice = inputElement.value;

        fetch(`/update_price/${productId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ price: newPrice }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the price in the table
                const grandparentElement = this.parentElement.parentElement;
                console.log(grandparentElement);  // Log the grandparent element to the console
                const priceElement = grandparentElement.querySelector('.product-price');
                if (priceElement) {
                    priceElement.textContent = newPrice;
                } else {
                    console.error('Element with class "product-price" not found within:', grandparentElement);
                }
            } else {
                // Show an error message
                console.error('Error:', data.error);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});