// const communityId = e.target.dataset.communityId
// const commentId = e.target.dataset.commentId
const commentButton = document.getElementById("comment-menu-button");

commentButton.addEventListener('click', () => {
const commentDropdown = document.getElementById("comment-dropdown");
commentDropdown.style.display = 'block';
});

commentButton.addEventListener('blur', () => {
    const commentDropdown = document.getElementById("comment-dropdown");
    
    // 0.2초 뒤에 실행
    setTimeout(() => {
    commentDropdown.style.display = 'none';
    }, 200);
});