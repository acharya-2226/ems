document.addEventListener("DOMContentLoaded", function() {
    const dropdown = document.querySelector(".dropbtn");
    const content = document.querySelector(".dropdown-content");

    dropdown.addEventListener("click", () => {
        content.style.display = content.style.display === "block" ? "none" : "block";
    });

    window.addEventListener("click", function(event) {
        if (!event.target.matches('.dropbtn')) {
            if (content.style.display === "block") {
                content.style.display = "none";
            }
        }
    });
});
