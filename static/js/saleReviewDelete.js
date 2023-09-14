const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
function deleteReview(event, product_pk, review_pk) {
  event.preventDefault();
  if (confirm('리뷰를 삭제하시겠습니까?')) {
    fetch(`/sales/${product_pk}/reviews/${review_pk}/delete_review/`, {
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