const noticeButton = document.getElementById("notice-menu-button");

noticeButton.addEventListener('click', () => {
const noticeDropdown = document.getElementById("notice-dropdown");
noticeDropdown.style.display = 'block';
});

noticeButton.addEventListener('blur', () => {
    const noticeDropdown = document.getElementById("notice-dropdown");
    
    // 0.2초 뒤에 실행
    setTimeout(() => {
    noticeDropdown.style.display = 'none';
    }, 200);
});