const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
function deleteComment(event, community_pk, community_comment_pk) {
  event.preventDefault();
  if (confirm('댓글을 삭제하시겠습니까?')) {
    fetch(`/communities/${community_pk}/community_comments/${community_comment_pk}/community_comment_delete/`, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': csrftoken,
      },
    })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('서버 에러');
      }
    })
    .then(data => {
      if (data.status === 'ok') {
        // Reload the page to reflect the updated comments
        location.reload();
      } else {
        alert(data.message);
      }
    })
    .catch(error => {
      alert(error.message);
    });
  }
}