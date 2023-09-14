const followersModal = document.getElementById("followers-modal")
const followersBtnModal = document.getElementById("followers-count")
const followersBackground = document.getElementById("followers-bg")
followersBtnModal.addEventListener("click", e => {
    followersModal.style.display = "flex"
})

followersModal.addEventListener("click", e => {
    const evTarget = e.target
    if(evTarget.classList.contains("modal-overlay")) {
        followersModal.style.display = "none"
    }
})

followersBackground.addEventListener("click", () => {
    followersModal.style.display = "none"
})

window.addEventListener("keyup", e => {
    if(followersModal.style.display === "flex" && e.key === "Escape") {
        followersModal.style.display = "none"
    }
})


const followingsModal = document.getElementById("followings-modal")
const followingsBtnModal = document.getElementById("followings-count")
const followingsBackground = document.getElementById("followings-bg")
followingsBtnModal.addEventListener("click", e => {
    followingsModal.style.display = "flex"
})

followingsModal.addEventListener("click", e => {
    const evTarget = e.target
    if(evTarget.classList.contains("modal-overlay")) {
        followingsModal.style.display = "none"
    }
})

followingsBackground.addEventListener("click", () => {
    followingsModal.style.display = "none"
})

window.addEventListener("keyup", e => {
    if(followingsModal.style.display === "flex" && e.key === "Escape") {
        followingsModal.style.display = "none"
    }
})