const moreButton = document.getElementById("more_dropdown_button");
const moreDropdown = document.getElementById("more_dropdown");

moreButton.addEventListener('mousedown', (event) => {
    event.preventDefault(); // 추가
    moreDropdown.style.display = moreDropdown.style.display === 'block' ? 'none' : 'block';
});

document.addEventListener('mouseup', (event) => {
    if (!moreButton.contains(event.target) && !moreDropdown.contains(event.target)) {
        moreDropdown.style.display = 'none';
    }
});

moreDropdown.addEventListener('click', (event) => {
    if (event.target.tagName === 'A') {
        moreDropdown.style.display = 'none';
    }
});
