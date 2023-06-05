const gardenLikeForms = document.querySelectorAll(".garden-like_forms");
const gardenCsrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

gardenLikeForms.forEach((form) => {
form.addEventListener('submit', function(e) {
    e.preventDefault()
    const gardenId = e.target.dataset.gardenId
    axios({
    method: 'post',
    url: `/gardens/${gardenId}/like_garden/`,
    headers: { "X-CSRFToken": gardenCsrfToken},
    }).then((response) => {
    const isLiked = response.data.is_liked;
    const likeCount = response.data.like_count;
    const likeBtn = document.getElementById('garden-like-btn');
    const likeCountTag = document.getElementById('garden-like-count');
    if (isLiked){
        likeBtn.classList.add('text-red-600');
        likeBtn.classList.remove('text-gray-500');
        likeCountTag.innerText = likeCount;
    } else {
        likeBtn.classList.add('text-gray-500');
        likeBtn.classList.remove('text-red-600');
        likeCountTag.innerText = likeCount;
    }
    })
    .catch((error) => {
    console.error(response.data);
    })
})
})
