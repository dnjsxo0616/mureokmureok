const logButton = document.getElementById("log-menu-button");

logButton.addEventListener('click', () => {
const logDropdown = document.getElementById("log-dropdown");
logDropdown.style.display = 'block';
});

logButton.addEventListener('blur', () => {
    const logDropdown = document.getElementById("log-dropdown");
    
    // 0.2초 뒤에 실행
    setTimeout(() => {
    logDropdown.style.display = 'none';
    }, 200);
});