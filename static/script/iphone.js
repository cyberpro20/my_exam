document.addEventListener('DOMContentLoaded', function () {
    updateCartCount();
});

function updateCartCount() {
    fetch('/get_cart_count/')
        .then(response => response.json())
        .then(data => {
            const cartCountElement = document.querySelector('.get_cart_count');
            cartCountElement.textContent = ` (${data.cart_count})`;
        })
        .catch(error => {
            console.error('Error fetching cart count:', error);
        });
}

function add_to_cart(iphone_id) {
    var formData = new FormData();
    formData.append('iphone_id', iphone_id);

    var csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch("/add_to_cart/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Товар успішно доданий до корзини!");
            updateCartCount();
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error("Помилка:", error));
}
