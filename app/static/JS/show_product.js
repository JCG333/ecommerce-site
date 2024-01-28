// =============== add item to cart =================

// event lisenter for creating orderItem button
document.getElementById('add-to-cart-form').addEventListener('submit', function () {
    var quantity = document.getElementById('quantity').value;
    var productId = document.querySelector('.product-container').dataset.productId;
    add_to_order(productId, quantity);
});

function add_to_order(id, quantity) {
    fetch(`/create_orderItem`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                product_id: id,
                quantity: quantity
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
            document.getElementById('orderItem_creation_action_response').textContent = 'item added to cart!';
        })
        // Error handling
        .catch(error => {
            document.getElementById('orderItem_creation_action_response').textContent = error.message;
        });
}


// ================ logo redirect =================

// event lisenter for logo redirect
document.getElementById('logo').addEventListener('click', function () {
    logo_redirect();
});

function logo_redirect() {
    window.location.replace('/');
}


// =================== register redirect ===================

// event lisenter for logo redirect
document.getElementById('register_button').addEventListener('click', function () {
    register_redirect();
});

function register_redirect() {
    window.location.replace('/register');
}


// =================== login form functionality =====================

// Close the dropdown if the user clicks outside of it
window.addEventListener('click', function () {
    var dropdownContent = document.getElementById('loginDropdown');
    dropdownContent.style.display = "none"; // Hide the dropdown when anywhere else on the window is clicked
});

document.getElementById('account-icon').addEventListener('click', function (event) {
    var dropdownContent = document.getElementById('loginDropdown');
    if (dropdownContent.style.display === "none") {
        dropdownContent.style.display = "block";
    } else {
        dropdownContent.style.display = "none";
    }
    event.stopPropagation();
});


// ===================== login form LOGIN ========================

// event lisenter for login button
document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the form from being submitted normally
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    login(email, password);
});

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
            document.getElementById('orderItem_creation_action_response').textContent = 'User logged in successfully!';
            document.getElementById('user-name').textContent = data.username; // Display the user's name
        })
        // Error handling
        .catch(error => {
            document.getElementById('orderItem_creation_action_response').textContent = error.message;
        });
}


window.onload = function () {
    fetch('/get_username')
        .then(response => response.json())
        .then(data => {
            if (data.username) {
                document.getElementById('user-name').textContent = data.username; // Display the user's name
            }
        });
};