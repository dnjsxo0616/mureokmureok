const cartButton = document.getElementById("cart-button");
const cartDropdown = document.getElementById("cart-dropdown");

cartButton.addEventListener('click', () => {
    cartDropdown.style.display = 'block';
});

cartButton.addEventListener('blur', () => {
    setTimeout(() => {
        cartDropdown.style.display = 'none';
    }, 200);
});

cartDropdown.addEventListener('click', (event) => {
    if (event.target.tagName === 'A') {
        cartDropdown.style.display = 'none';
    }
});