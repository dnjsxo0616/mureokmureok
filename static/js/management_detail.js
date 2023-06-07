const entryModal = document.getElementById("entry-create-modal")
const entryBtnModal = document.getElementById("entry-create-btn")
const entryBackground = document.getElementById("entry-bg")
entryBtnModal.addEventListener("click", e => {
  entryModal.style.display = "flex"
})

entryModal.addEventListener("click", e => {
  const evTarget = e.target
  if(evTarget.classList.contains("modal-overlay")) {
    entryModal.style.display = "none"
  }
})

entryBackground.addEventListener("click", () => {
  entryModal.style.display = "none"
})

window.addEventListener("keyup", e => {
  if(entryModal.style.display === "flex" && e.key === "Escape") {
    entryModal.style.display = "none"
  }
})