
const managementButton = document.getElementById("management-menu-button");

managementButton.addEventListener('click', () => {
const managementDropdown = document.getElementById("management-dropdown");
managementDropdown.style.display = 'block';
});

managementButton.addEventListener('blur', () => {
    const managementDropdown = document.getElementById("management-dropdown");
    
    // 0.2초 뒤에 실행
    setTimeout(() => {
        managementDropdown.style.display = 'none';
    }, 20);
});
