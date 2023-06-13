const entryModal = document.getElementById("entry-create-modal")
const entryBtnModal = document.getElementById("entry-create-btn")
const entryBackground = document.getElementById("entry-bg")
entryBtnModal.addEventListener("click", e => {
  entryModal.style.display = "flex"
})

entryModal.addEventListener("click", e => {
  const evTarget = e.target
  if(evTarget.classList.contains("modal-overlay")) {
    entryModal.style.display = "none"
  }
})

entryBackground.addEventListener("click", () => {
  entryModal.style.display = "none"
})

window.addEventListener("keyup", e => {
  if(entryModal.style.display === "flex" && e.key === "Escape") {
    entryModal.style.display = "none"
  }
})


const entryUpdateModals = document.querySelectorAll(".entry-update-modal");
const entryUpdateBtns = document.querySelectorAll(".entry-update-btn");
const entryUpdateBackground = document.getElementById("entry-update-bg");

entryUpdateBtns.forEach((btn, index) => {
  btn.addEventListener("click", () => {
    const modal = entryUpdateModals[index];
    modal.style.display = "flex";
  });
});


entryUpdateModals.forEach((modal, index) => {
  modal.addEventListener("click", (e) => {
    if (e.target.classList.contains("modal-overlay")) {
      modal.style.display = "none";
    }
  });

  entryUpdateBackground.addEventListener("click", () => {
    modal.style.display = "none";
  });

  window.addEventListener("keyup", (e) => {
    if (modal.style.display === "flex" && e.key === "Escape") {
      modal.style.display = "none";
    }
  });
});







var today = new Date();



  // 캘린더 생성 함수
  function createCalendar(year, month) {
    // 캘린더를 표시할 요소
    var calendarElement = document.getElementById("calendar");

    // 요일 헤더 생성
    var headerRow = document.createElement("div");
    headerRow.classList.add("grid", "grid-cols-7", "gap-4");
    var daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    daysOfWeek.forEach(function (dayOfWeek) {
      var headerCell = document.createElement("div");
      headerCell.classList.add("col-span-1", "text-center", "font-bold");
      headerCell.textContent = dayOfWeek;
      headerRow.appendChild(headerCell);
    });
    calendarElement.appendChild(headerRow);

    // 해당 월의 첫 번째 날의 요일과 날짜 수 가져오기
    var firstDayOfMonth = new Date(year, month, 1);
    var firstDayOfWeek = firstDayOfMonth.getDay();
    var numDaysInMonth = new Date(year, month + 1, 0).getDate();

    // 캘린더 내용 생성
    var calendarDays = [];
    var weekData = [];
    for (var i = 0; i < firstDayOfWeek; i++) {
      weekData.push(null);
    }
    for (var day = 1; day <= numDaysInMonth; day++) {
      var date = new Date(year, month, day);
      var entryData = entries.find(function(entry) {
        return new Date(entry.entrydate).toDateString() === date.toDateString();
      });
      weekData.push({ date: date, entryData: entryData });
      if (weekData.length === 7) {
        calendarDays.push(weekData);
        weekData = [];
      }
    }
    if (weekData.length > 0) {
      calendarDays.push(weekData);
    }

    // 캘린더 날짜 표시
    calendarDays.forEach(function (weekData) {
      var weekRow = document.createElement("div");
      weekRow.classList.add("grid", "grid-cols-7", "gap-4");
      weekData.forEach(function (data) {
        var dayCell = document.createElement("div");
        dayCell.classList.add("col-span-1", "border", "border-gray-300", "p-2");
        if (data) {
          var date = data.date;
          var entryData = data.entryData;
          dayCell.textContent = date.getDate();
          if (entryData) {
            var entryDiv = document.createElement("div");
            entryDiv.textContent = "Watering: " + entryData.fields.watering + ", Sunlight: " + entryData.fields.sunlight + ", Humidity: " + entryData.fields.humidity + ", Temperature: " + entryData.fields.temperature;
            dayCell.appendChild(entryDiv);
            
          }
        }
        weekRow.appendChild(dayCell);
      });
      calendarElement.appendChild(weekRow);
    });
  }

  // 캘린더 생성 호출
  createCalendar(today.getFullYear(), today.getMonth(), JSON.parse('{{ entries_json|safe }}'));


  