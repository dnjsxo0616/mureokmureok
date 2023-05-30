const modal = document.getElementById("followers-modal")
const btnModal = document.getElementById("followers-count")
btnModal.addEventListener("click", e => {
    modal.style.display = "flex"
})

modal.addEventListener("click", e => {
    const evTarget = e.target
    if(evTarget.classList.contains("modal-overlay")) {
        modal.style.display = "none"
    }
})

window.addEventListener("keyup", e => {
    if(modal.style.display === "flex" && e.key === "Escape") {
        modal.style.display = "none"
    }
})