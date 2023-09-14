const gardenButton = document.getElementById("garden-menu-button");

gardenButton.addEventListener('click', () => {
const gardenDropdown = document.getElementById("garden-dropdown");
gardenDropdown.style.display = 'block';
});

gardenButton.addEventListener('blur', () => {
    const gardenDropdown = document.getElementById("garden-dropdown");
    
    // 0.2초 뒤에 실행
    setTimeout(() => {
    gardenDropdown.style.display = 'none';
    }, 200);
});