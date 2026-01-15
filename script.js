document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
        toggle.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();

            const menu = this.nextElementSibling;

            document.querySelectorAll('.dropdown-menu').forEach(dropdown => {
                if (dropdown !== menu) {
                    dropdown.classList.remove('active');
                }
            });

            menu.classList.toggle('active');
        });
    });

    document.addEventListener('click', function (e) {
        if (!e.target.closest('.nav-item')) {
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.classList.remove('active');
            });
        }
    });
});

document.addEventListener("submit", function () {
    e.preventDefault(); // stop page reload

    const email = document.getElementById("email").value;

    fetch("http://127.0.0.1:5500/newsletter", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email: email })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById("newsletterForm").reset();
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to subscribe");
    });
});
