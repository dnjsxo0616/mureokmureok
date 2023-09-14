const saleLikeForms = document.querySelectorAll(".sale-like_forms");
const saleCsrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

saleLikeForms.forEach((form) => {
form.addEventListener('submit', function(e) {
    e.preventDefault()
    const productId = e.target.dataset.productId
    axios({
    method: 'post',
    url: `/sales/${productId}/like/`,
    headers: { "X-CSRFToken": saleCsrfToken},
    }).then((response) => {
        const isLiked = response.data.is_liked;
        const likeCount = response.data.like_count;
        const likeBtn = document.getElementById('sale-like-btn');
        const likeCountTag = document.getElementById('sale-like-count');
        if (isLiked) {
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
