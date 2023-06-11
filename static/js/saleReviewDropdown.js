// const communityId = e.target.dataset.communityId
// const commentId = e.target.dataset.commentId
const reviewButton = document.getElementById("review-menu-button");

reviewButton.addEventListener('click', () => {
const reviewDropdown = document.getElementById("review-dropdown");
reviewDropdown.style.display = 'block';
});

reviewButton.addEventListener('blur', () => {
    const reviewDropdown = document.getElementById("review-dropdown");
    
    // 0.2초 뒤에 실행
    setTimeout(() => {
    reviewDropdown.style.display = 'none';
    }, 200);
});