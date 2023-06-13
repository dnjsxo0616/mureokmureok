const shareButton = document.getElementById("share-menu-button");
const shareDropdown = document.getElementById("share-dropdown");

shareButton.addEventListener('mousedown', (event) => {
    event.preventDefault(); // 추가
    shareDropdown.style.display = shareDropdown.style.display === 'block' ? 'none' : 'block';
});

document.addEventListener('mouseup', (event) => {
    if (!shareButton.contains(event.target) && !shareDropdown.contains(event.target)) {
        shareDropdown.style.display = 'none';
    }
});

shareDropdown.addEventListener('click', (event) => {
    if (event.target.tagName === 'A') {
        shareDropdown.style.display = 'none';
    }
});
