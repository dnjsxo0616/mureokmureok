const pro_button = document.getElementById("user-menu-button");
const pro_dropdown = document.getElementById("profile-dropdown");

pro_button.addEventListener('click', () => {
    pro_dropdown.style.display = 'block';
});

pro_button.addEventListener('blur', () => {
    setTimeout(() => {
        pro_dropdown.style.display = 'none';
    }, 200);
});

pro_dropdown.addEventListener('click', (event) => {
    if (event.target.tagName === 'A') {
        pro_dropdown.style.display = 'none';
    }
});