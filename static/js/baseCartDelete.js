const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
function deleteCart(event, product_pk) {
event.preventDefault();

fetch(`/sales/remove-from-cart/${product_pk}/`, {
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
