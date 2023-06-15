var link =  window.location.href;
var sendText = document.getElementById('plant-title').innerText; // 전달할 텍스트

function shareTwitter2() {
    var sendUrl = link; // 전달할 URL
    window.open("https://twitter.com/intent/tweet?text=" + sendText + "&url=" + sendUrl);
}

function shareFacebook2() {
    var sendUrl = link; // 전달할 URL
    window.open("http://www.facebook.com/sharer/sharer.php?u=" + sendUrl);
}


function shareLink2() {
    navigator.clipboard.writeText(link)
        .then(function() {
            alert('현재 페이지의 링크가 복사되었습니다.');
        })
        .catch(function(err) {
            console.error('링크 복사 실패', err);
        });
}