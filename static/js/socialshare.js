var link =  window.location.href;
var gardenTitle = document.getElementById('garden-title').innerText; // 전달할 식물원이름
var sendText = document.getElementById('garden-content').innerText; // 전달할 텍스트

function shareTwitter() {
    var sendUrl = link; // 전달할 URL
    window.open("https://twitter.com/intent/tweet?text=" + sendText + "&url=" + sendUrl);
}

function shareFacebook() {
    var sendUrl = link; // 전달할 URL
    window.open("http://www.facebook.com/sharer/sharer.php?u=" + sendUrl);
}

// function shareKakao() {

//     // 사용할 앱의 JavaScript 키 설정
//     Kakao.init('da98acbaa78a8dc3692f2a550e4da234');

//     Kakao.Share.sendDefault({
//         objectType: 'feed',
//         content: {
//             title: movieTitle, // 보여질 제목
//             description: sendText, // 보여질 설명
//             imageUrl: link, // 콘텐츠 URL
//             link: {
//                 mobileWebUrl: link,
//                 webUrl: link
//             }
//         }
//     });
// }

function shareLink() {
    navigator.clipboard.writeText(link)
        .then(function() {
            alert('현재 페이지의 링크가 복사되었습니다.');
        })
        .catch(function(err) {
            console.error('링크 복사 실패', err);
        });
}