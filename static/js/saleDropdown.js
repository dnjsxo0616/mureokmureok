const saleButton = document.getElementById("sale-menu-button");
const saleDropdown = document.getElementById("sale-dropdown");

saleButton.addEventListener('mousedown', (event) => {
    event.preventDefault(); // 추가
    saleDropdown.style.display = saleDropdown.style.display === 'block' ? 'none' : 'block';
});

document.addEventListener('mouseup', (event) => {
    if (!saleButton.contains(event.target) && !saleDropdown.contains(event.target)) {
        saleDropdown.style.display = 'none';
    }
});

saleDropdown.addEventListener('click', (event) => {
    if (event.target.tagName === 'A') {
        saleDropdown.style.display = 'none';
    }
});
