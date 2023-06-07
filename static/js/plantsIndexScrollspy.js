// 윈도우 스크롤 이벤트 (스크롤을 했을 때 발생)
window.addEventListener("scroll", () => {
    // 1. 섹션들을 querySelectorAll을 통해 변수에 담는다.
    const sections = document.querySelectorAll("section");
    // 2. scrollspy 메뉴들을 querySelectorAll을 통해 변수에 담는다.
    const scrollItems = document.querySelectorAll(".scrollspy-item");

    // 3. forEach 문을 통해 섹션들을 한번씩 순회한다.
    // 이때 index도 같이 가져온다.
    sections.forEach((section, index) => {
    const top = window.scrollY; //현재 Y값
    const sectionTop = section.offsetTop - 40; // 섹션 상단의 Y값 - Gnb메뉴 높이 값
    const sectionHeight = section.offsetHeight; // 섹션 높이

    // 4. forEach 문을 통해 scrollspy 메뉴들을 한번씩 순회한다.
    scrollItems.forEach((scrollItem) => {
        // 5. 스크롤 위치가 섹션 상단 스크롤 위치보다 크고 && 섹션높이값보다 작을 경우
        if (top >= sectionTop && top < sectionTop + sectionHeight) {
        // 6. scrollspy 메뉴들의 active 클래스를 전부 지운다.
        scrollItem.classList.remove("text-black", "font-semibold");
        // 7. 해당 index에 해당하는 scrollspy 메뉴의 클래스에만 active 클래스명을 추가한다.
        scrollItems[index].classList.add("text-black", "font-semibold");
        }
    });
    });
});
