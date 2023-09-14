const button = document.getElementById("user-menu-button");
const dropdown = document.getElementById("profile-dropdown");

button.addEventListener('click', () => {
    dropdown.style.display = 'block';
});

button.addEventListener('blur', () => {
    setTimeout(() => {
        dropdown.style.display = 'none';
    }, 200);
});

dropdown.addEventListener('click', (event) => {
    if (event.target.tagName === 'A') {
        dropdown.style.display = 'none';
    }
});