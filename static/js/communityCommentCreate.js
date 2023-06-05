const Community_commentForm = document.querySelector('#Community_comment-Form')

Community_commentForm.addEventListener('submit', function (event) {
  event.preventDefault();

  const formData = new FormData(Community_commentForm)

  axios({
    method: 'post',
    url: Community_commentForm.getAttribute('action'),
    data: formData,
  })
    .then((response) => {
      location.reload();
    })
    .catch((error) => {
      console.log(error.response.data);
    })
})