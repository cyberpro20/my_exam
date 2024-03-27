
function editProfile() {
    var editBtn = document.getElementById("edit-profile-btn");
    var form = document.getElementById("profile-form");
    var saveBtn = document.getElementById("update-profile-btn");

    if (form.style.display === "none") {
        form.style.display = "block";
        editBtn.style.display = "none";
        saveBtn.style.display = "inline-block";
    } else {
        form.style.display = "none";
        editBtn.style.display = "inline-block";
        saveBtn.style.display = "none";
    }
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


document.getElementById("profile-form").addEventListener("submit", function(event) {
    event.preventDefault();
    var formData = new FormData(this);

    fetch("{% url 'update_profile' %}", {
        method: "POST",
        body: formData,
        headers: {
        }
    })
    .then(response => response.json())
    .then(data => {
        alert("Інформація успішно оновлена!");
        location.reload(); // Оновлення сторінки
    })
    .catch(error => console.error("Помилка:", error));
});


