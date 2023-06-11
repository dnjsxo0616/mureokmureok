const searchInput = document.querySelector('#plant-search');
const selectField = document.querySelector('#plant-select');
const options = Array.from(selectField.options);

searchInput.addEventListener('input', function() {
  const searchTerm = this.value.toLowerCase();

  options.forEach(option => {
    const label = option.textContent.toLowerCase();
    if (label.includes(searchTerm)) {
      option.hidden = false;
    } else {
      option.hidden = true;
    }
  });
});

selectField.addEventListener('change', function() {
  const selectedValue = this.value;

  if (selectedValue === '') {
    searchInput.classList.remove('hidden');
  } else {
    searchInput.classList.add('hidden');
  }
});