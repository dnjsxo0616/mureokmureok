const commentModal = document.getElementById("comment-create-modal")
const commentBtnModal = document.getElementById("comment-create-btn")
const commentBackground = document.getElementById("comment-bg")
commentBtnModal.addEventListener("click", e => {
    commentModal.style.display = "flex"
})

commentModal.addEventListener("click", e => {
    const evTarget = e.target
    if(evTarget.classList.contains("modal-overlay")) {
        commentModal.style.display = "none"
    }
})

commentBackground.addEventListener("click", () => {
    commentModal.style.display = "none"
})

window.addEventListener("keyup", e => {
    if(commentModal.style.display === "flex" && e.key === "Escape") {
        commentModal.style.display = "none"
    }
})