function showiPhoneModels() {
    document.getElementById("iphone-dropdown").style.display = "block";
}

function hideiPhoneModels() {
    document.getElementById("iphone-dropdown").style.display = "none";
}

document.addEventListener('DOMContentLoaded', function() {
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