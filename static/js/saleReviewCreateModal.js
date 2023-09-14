const reviewModal = document.getElementById("review-create-modal")
const reviewBtnModal = document.getElementById("review-create-btn")
const reviewBackground = document.getElementById("review-bg")
reviewBtnModal.addEventListener("click", e => {
    reviewModal.style.display = "flex"
})

reviewModal.addEventListener("click", e => {
    const evTarget = e.target
    if(evTarget.classList.contains("modal-overlay")) {
        reviewModal.style.display = "none"
    }
})

reviewBackground.addEventListener("click", () => {
    reviewModal.style.display = "none"
})

window.addEventListener("keyup", e => {
    if(reviewModal.style.display === "flex" && e.key === "Escape") {
        reviewModal.style.display = "none"
    }
})