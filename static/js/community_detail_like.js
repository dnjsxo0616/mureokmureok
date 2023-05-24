const forms = document.querySelectorAll(".like-form")
const csrftokenLike = document.querySelector("[name=csrfmiddlewaretoken]").value

forms.forEach((form) => {
  form.addEventListener('submit', function(e) {
    e.preventDefault()
    const communityId = e.target.dataset.communityId
    axios({
      method: 'post',
      url: `/communities/${communityId}/likes/`,
      headers: { "X-CSRFToken": csrftokenLike},
    }).then((response) => {
      const isLiked = response.data.is_liked
      const likeBtn = form.querySelector(`#like-btn`)
      if (isLiked){
        likeBtn.className = 'heart-fill'
      } else{
        likeBtn.className = 'heart'
      }

      const likeCountTag = form.querySelector('#like-count')
      const likeCountData = response.data.like_count
      likeCountTag.textContent = likeCountData
    })
    .catch((error) => {
      console.log(error.response)
    })
  })
})
