// 탭 요소들을 선택합니다.
const tabs = document.querySelectorAll('.tab');

// 탭 클릭 이벤트를 처리하는 함수입니다.
function handleTabClick() {
// 모든 탭에 active 클래스를 제거합니다.
tabs.forEach(tab => tab.classList.remove('active'));

// 클릭한 탭에 active 클래스를 추가합니다.
this.classList.add('active');

// 클릭한 탭의 인덱스를 가져옵니다.
const tabIndex = Array.from(tabs).indexOf(this);

// 모든 컨텐츠를 숨깁니다.
const contents = document.querySelectorAll('.content');
const supplies = document.querySelectorAll('.supply');
contents.forEach(content => content.style.display = 'none');
supplies.forEach(supply => supply.style.display = 'none');

// 클릭한 탭에 해당하는 컨텐츠를 보여줍니다.
contents[tabIndex].style.display = 'block';
supplies[tabIndex].style.display = 'block';
}

// 각 탭에 클릭 이벤트를 등록합니다.
tabs.forEach(tab => tab.addEventListener('click', handleTabClick));

// 초기에 첫 번째 탭을 선택 상태로 만듭니다.
tabs[0].click();