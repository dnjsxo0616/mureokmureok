const forms = document.querySelectorAll('.like-forms');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

forms.forEach((form) => {
    form.addEventListener('submit', function (event) {
        event.preventDefault()
        const plantId = event.target.dataset.plantId
        axios({
        method: 'post',
        url: `/plants/${plantId}/likes/`,
        headers: {'X-CSRFTOKEN': csrftoken},
        }).then((response) => {
            const isLiked = response.data.is_liked;
            const likeCount = response.data.like_count;
            const likeBtn = document.querySelector(`#like-${plantId}`);
            const likeCountTag = document.getElementById('plant-like-count');
            if (isLiked === true) {
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
            console.log(error.response)
        })
    })
})
