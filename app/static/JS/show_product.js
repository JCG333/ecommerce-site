// =============== add item to cart =================

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
            showError('item added to cart!', true);
        })
        // Error handling
        .catch(error => {
            showError(error.message, false);
        });
}
// event lisenter for creating orderItem button
document.getElementById('add-to-cart-form').addEventListener('submit', function () {
    var quantity = document.getElementById('quantity').value;
    var productId = document.querySelector('.product-container').dataset.productId;
    add_to_order(productId, quantity);
    updateCartNotification();
});


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
            showError('logout success!', true);
            document.getElementById('user-name').textContent = '';
            updateCartNotification();
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

// =================== PRODUCT SPECIFIC =====================

// =================== get reviews =====================

function get_reviews(product_id) {
    fetch(`/reviews/${product_id}`)
        // check if response is OK
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => Promise.reject(error));
            }
            return response.json();
        })
        // if OK
        .then(data => {
            var dropdown = document.getElementById('reviewsDropdown');
            // Clear previous options
            dropdown.innerHTML = '';

            if (data.reviews) {
                data.reviews.forEach(review => {
                    var item = document.createElement('a');
                    item.href = '#';
                    var date = new Date(review.created_at);
                    var formattedDate = date.getFullYear() + '-' + String(date.getMonth() + 1).padStart(2, '0') + '-' + String(date.getDate()).padStart(2, '0');
                    item.innerHTML = '[' + formattedDate + '] ' + '<strong>' + review.user_name + '</strong>' + ': ' + review.comment + ' - ' + '★'.repeat(review.rating);
                    item.style.display = 'block';
                    dropdown.appendChild(item);
                });
            }
        })// Error handling
        .catch(error => {
            showError(error.message, false);
        });
}
// Add event listener to the dropdown
document.getElementById('reviewsButton').addEventListener('click', function () {
    var dropdown = document.getElementById('reviewsDropdown');
    dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
    var product_id = document.querySelector('.review-container').dataset.reviewId;
    get_reviews(product_id);
});

// =================== post review =====================

function post_review(product_id, comment, rating) {
    fetch(`/post_review/${product_id}`,
        {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                comment: comment,
                rating: rating
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
            showError('Review posted successfully!', true);
        })
        // Error handling
        .catch(error => {
            showError(error.message, false);
        });
}
// Add event listener to the form
document.getElementById('review-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the form from being submitted normally
    var comment = document.getElementById('review').value;
    var product_id = document.querySelector('.review-container').dataset.reviewId;
    // Select the radio buttons
    var ratings = document.getElementsByName('rating');

    // Initialize a variable to store the selected rating
    var selectedRating;

    // Loop through the radio buttons
    for (var i = 0; i < ratings.length; i++) {
        // If the radio button is checked
        if (ratings[i].checked) {
            // Store the value of the checked radio button
            selectedRating = ratings[i].value;

            // Break the loop
            break;
        }
    }
    post_review(product_id, comment, selectedRating);
});

// ================ get average rating ==================
function updateAverageRating(productId) {
    fetch('/average_rating/' + productId)
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => Promise.reject(error));
            }
            return response.json();
        })
        // if OK
        .then(data => {
            // Update the #average_rating element with the new rating
            var averageRatingElement = document.getElementById('average_rating');
            averageRatingElement.textContent = 'Average Rating: ' + data.average;

            // Clear the stars
            while (averageRatingElement.firstChild) {
                averageRatingElement.removeChild(averageRatingElement.firstChild);
            }

            // Add the new stars
            for (var i = 0; i < data.average; i++) {
                var star = document.createElement('span');
                star.textContent = '★';
                averageRatingElement.appendChild(star);
            }
            // add number of reviews
            updateNumberOfReviews(productId);
        })
        // Error handling
        .catch(error => {
            showError(error.message, false);
        });
}
//get number of reviews
function updateNumberOfReviews(productId) {
    fetch('/number_of_reviews/' + productId)
        // check if response is OK
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => Promise.reject(error));
            }
            return response.json();
        })
        // if OK
        .then(data => {
            // Update the #average_rating element with the new rating
            var averageRatingElement = document.getElementById('average_rating');
            var reviews_num = document.createElement('span');
            reviews_num.textContent = '(' + data.number_of_reviews + ')';
            if (data.number_of_reviews > 0) {
                averageRatingElement.appendChild(reviews_num);
            }
            else {
                reviews_num.textContent = '(no reviews)';
                averageRatingElement.appendChild(reviews_num);
            }
        })
        // Error handling
        .catch(error => {
            showError(error.message, false);
        });
}

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
            return response.json();
        })
        // if OK
        .then(data => {
            if (data.order_size > 0) {
                document.getElementById('round-div').textContent = data.order_size;
            } else {
                document.getElementById('round-div').textContent = 0;
            }
        })
        // Error handling
        .catch(error => {
            console.log('Error fetching order size: ' + error);
        });
}

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
    var productId = document.querySelector('.product-container').dataset.productId;
    updateAverageRating(productId);
    updateCartNotification();
};
