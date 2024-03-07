// ========== FORMATTING EXPERY DATE ========== //
document.getElementById("expiry_date").addEventListener("input", function(e) {
    var input = e.target;
    var value = input.value.replace(/\D/g, '').substring(0, 4);
    var formattedValue = value.replace(/^(\d\d)(\d)/g, '$1/$2');
    input.value = formattedValue;
});

// ========== FORMATTING CARD NUMBER ========== //
document.getElementById("card_number").addEventListener("input", function(e) {
    var input = e.target;
    var value = input.value.replace(/\s+/g, '').replace(/[^0-9\s]/gi, '');
    var formattedValue = value.replace(/(.{4})/g, '$1 ').trim();
    input.value = formattedValue;
});

// ========== FORMATTING CVV ========== //
document.getElementById("cvv").addEventListener("input", function(e) {
    var input = e.target;
    input.value = input.value.replace(/\D/g, '');
});

// ========== shipping ========== //
document.getElementById("country").addEventListener("input", function(e) {
    var input = e.target;
    input.value = input.value;
});
document.getElementById("address").addEventListener("input", function(e) {
    var input = e.target;
    input.value = input.value;
});

// redirect to completion
document.getElementById('payment-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var ordersElement = document.getElementById('orderID');
    var orderId = ordersElement.getAttribute('data-order-id');

    this.action = '/add_shipping/'+ orderId +'/' + document.getElementById('country').value +'/'+document.getElementById('address').value;
    this.submit();
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
};