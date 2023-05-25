const button = document.getElementById("user-menu-button");

button.addEventListener('click', () => {
const dropdown = document.getElementById("profile-dropdown");
dropdown.style.display = 'block';
});

button.addEventListener('blur', () => {
    const dropdown = document.getElementById("profile-dropdown");
    
    // 0.2초 뒤에 실행
    setTimeout(() => {
    dropdown.style.display = 'none';
    }, 200);
});