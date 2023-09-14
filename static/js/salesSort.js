var sort_type = 'popularity';  // 기본 정렬 기준
var load_data = function() {
    axios.get(`/sales/sort/?sort_type=${sort_type}`)
    .then(function(response) {
        var data = response.data;
        // 데이터 처리 및 HTML 동적 변경
    })
    .catch(function(error) {
        console.log(error);
    });
};

load_data();  // 페이지 로드 시, 초기 데이터 로딩

// 정렬 옵션 변경 시, 데이터 다시 로딩
$('.sort-option').on('click', function() {
    var option = $(this).data('value');
    sort_type = option;
    load_data();
});