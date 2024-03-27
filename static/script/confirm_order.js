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

// Функція для видалення товару з корзини
function removeItem(itemId) {
    fetch(`/remove_from_cart/${itemId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Отримання CSRF-токена
        },
    })
    .then(response => {
        if (response.ok) {
            // Якщо видалення пройшло успішно, оновити сторінку
            window.location.reload();
        } else {
            // Обробити помилку, якщо її повернув сервер
            console.error('Failed to remove item from cart');
        }
    })
    .catch(error => {
        // Обробити помилку запиту
        console.error('Error removing item from cart:', error);
    });
}

// Функція для отримання значення CSRF-токена з кукі
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
