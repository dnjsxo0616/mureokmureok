const community_comment_like_forms = document.querySelectorAll('.community_comment_like_forms')
const c_csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value
community_comment_like_forms.forEach(form => {
  form.addEventListener('submit', function (event) {  
    event.preventDefault()
    const communityId = event.target.dataset.communityId;
    const commentId = event.target.dataset.commentId;
    axios({
      method: 'post',
      url: `/communities/${communityId}/community_comments/${community_commentId}/community_comment_likes/`,
      headers: {'X-CSRFToken': c_csrfToken},
    })
    .then((response) => {
      const isLiked = response.data.c_is_like
      console.log(isLiked)
      const likeBtn = document.querySelector(`#community_comment-like-btn-${community_commentId}`)
      console.log(likeBtn)
      if (isLiked){
        likeBtn.className = "heart-fill"
      } else {likeBtn.className = "heart"}
      const likesCountData = response.data.c_like_count
      console.log(likesCountData)  // 여기로 옮깁니다.
      const likesCountTag = document.querySelector(`#c_likes_count_${community_commentId}`)
      console.log(likesCountTag)
      likesCountTag.textContent = likesCountData

      // location.reload();
    })
    // .catch((error) => {
    //   console.error(response.data);
    });
  });
// });

