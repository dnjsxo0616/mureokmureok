const communityLikeForms = document.querySelectorAll(".community-like_forms");
const communityCsrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

communityLikeForms.forEach((form) => {
  form.addEventListener('submit', function(e) {
    e.preventDefault()
    const communityId = e.target.dataset.communityId
    axios({
      method: 'post',
      url: `/communities/${communityId}/likes/`,
      headers: { "X-CSRFToken": communityCsrfToken},
    }).then((response) => {
      const isLiked = response.data.is_liked;
      const likeCount = response.data.like_count;
      const likeBtn = document.getElementById('community-like-btn');
      const likeCountTag = document.getElementById('community-like-count');
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
