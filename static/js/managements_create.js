$(document).ready(function() {
    // 플랜트 목록을 담고 있는 배열
    var plantList = [
      "플랜트1",
      "플랜트2",
      "플랜트3",
      // ...
    ];
  
    // 드롭다운 요소를 클릭하면 드롭다운 펼치기/접기
    $('.dropdown').click(function(e) {
      e.stopPropagation();
      $(this).toggleClass('active');
    });
  
    // 검색 입력창에 입력할 때마다 플랜트 목록 필터링
    $('input[type="text"]').on('input', function() {
      var searchTerm = $(this).val().toLowerCase();
      var filteredList = plantList.filter(function(plant) {
        return plant.toLowerCase().includes(searchTerm);
      });
  
      // 플랜트 목록 업데이트
      var plantListElement = $('.plant-list');
      plantListElement.empty();
      filteredList.forEach(function(plant) {
        var listItem = $('<li></li>').text(plant);
        listItem.click(function() {
          // 선택한 플랜트를 드롭다운에 적용
          var selectedPlant = $(this).text();
          $('.dropdown input[type="text"]').val(selectedPlant);
        });
        plantListElement.append(listItem);
      });
    });
  
    // 클릭 이벤트가 발생하면 드롭다운 닫기
    $(document).click(function() {
      $('.dropdown').removeClass('active');
    });
  });