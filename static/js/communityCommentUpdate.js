const commentUpdateModal = document.getElementById("comment-update-modal")
const commentUpdateBtnModal = document.getElementById("comment-update-btn")
const commentUpdateBackground = document.getElementById("comment-bg")
commentUpdateBtnModal.addEventListener("click", e => {
    commentUpdateModal.style.display = "flex"
})

commentUpdateModal.addEventListener("click", e => {
    const evTarget = e.target
    if(evTarget.classList.contains("modal-overlay")) {
        commentUpdateModal.style.display = "none"
    }
})

commentUpdateBackground.addEventListener("click", () => {
    commentUpdateModal.style.display = "none"
})

window.addEventListener("keyup", e => {
    if(commentUpdateModal.style.display === "flex" && e.key === "Escape") {
        commentUpdateModal.style.display = "none"
    }
})