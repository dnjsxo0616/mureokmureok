const plantButton = document.getElementById("plant-menu-button");

plantButton.addEventListener('click', () => {
const plantDropdown = document.getElementById("plant-dropdown");
plantDropdown.style.display = 'block';
});

plantButton.addEventListener('blur', () => {
    const plantDropdown = document.getElementById("plant-dropdown");
    
    // 0.2초 뒤에 실행
    setTimeout(() => {
        plantDropdown.style.display = 'none';
    }, 200);
});