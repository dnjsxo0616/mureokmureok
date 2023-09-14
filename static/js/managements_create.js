const plantSelect = document.getElementById('plant-select');
  const plantSearchInput = document.getElementById('plant-search-input');
  const plants = Array.from(document.querySelectorAll('#plant-select option'));

  plantSearchInput.addEventListener('input', () => {
    const searchTerm = plantSearchInput.value.toLowerCase();

    // 필터링된 식물 목록 업데이트
    const filteredPlants = plants.filter((plant) => {
      return plant.textContent.toLowerCase().includes(searchTerm);
    });

    // 기존 옵션 제거
    plantSelect.innerHTML = '';

    // 필터링된 식물 목록 추가
    filteredPlants.forEach((plant) => {
      plantSelect.appendChild(plant);
    });
  });