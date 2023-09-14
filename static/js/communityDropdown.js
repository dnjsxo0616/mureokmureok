const communityButton = document.getElementById("community-menu-button");

communityButton.addEventListener('click', () => {
const communityDropdown = document.getElementById("community-dropdown");
communityDropdown.style.display = 'block';
});

communityButton.addEventListener('blur', () => {
    const communityDropdown = document.getElementById("community-dropdown");
    
    // 0.2초 뒤에 실행
    setTimeout(() => {
    communityDropdown.style.display = 'none';
    }, 200);
});