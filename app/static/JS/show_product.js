// ===== add item to cart =====
function add_to_order(id, quantity) {
    fetch(`/create_orderItem`,
        {
            method: 'POST',
            body: JSON.stringify({
                id: id,
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
            document.getElementById('orderItem_creation_action_response').textContent = 'User created successfully!';
            get_users_data();
        })
        // Error handling
        .catch(error => {
            document.getElementById('orderItem_creation_action_response').textContent = error.message;
        });
}
// event lisnter for CREATE orderItem button
document.getElementById('create_orderItem_button').addEventListener('click', function () {
    var quantity = document.getElementById('quantity').value;
    var productId = button.dataset.id;
    add_to_order(productId, quantity);
});