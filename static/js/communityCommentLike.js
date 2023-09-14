const communityCommentLikeForms = document.querySelectorAll('.community_comment_like_forms');
const commentCsrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

communityCommentLikeForms.forEach(form => {
  form.addEventListener('submit', function (event) {  
    event.preventDefault()
    const communityId = event.target.dataset.communityId;
    const commentId = event.target.dataset.commentId;
    axios({
      method: 'post',
      url: `/communities/${communityId}/community_comments/${commentId}/community_comment_likes/`,
      headers: {'X-CSRFToken': commentCsrfToken},
    })
    .then((response) => {
      const isLiked = response.data.is_like;
      const likeCount = response.data.like_count;
      const likeBtn = document.getElementById(`comment-like-btn-${communityId}-${commentId}`)
      const commentLikeCount = document.getElementById(`comment-like-count-${communityId}-${commentId}`)
      if (isLiked) {
        likeBtn.classList.add('text-red-600');
        likeBtn.classList.remove('text-gray-500');
        commentLikeCount.innerText = likeCount;
      } else {
        likeBtn.classList.add('text-gray-500');
        likeBtn.classList.remove('text-red-600');
        commentLikeCount.innerText = likeCount;
      }
    })
    .catch((error) => {
      console.error(response.data);
    });
  });
});
