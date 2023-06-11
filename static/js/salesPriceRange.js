const inputLeft = document.getElementById("input-left");
const inputRight = document.getElementById("input-right");
const cntLeft = document.getElementById("cnt-left");
const cntRight = document.getElementById("cnt-right");

const thumbLeft = document.querySelector(".slider > .thumb.left");
const thumbRight = document.querySelector(".slider > .thumb.right");
const range = document.querySelector(".slider > .range");

const setLeftValue = () => {
const _this = inputLeft;
const [min, max] = [parseInt(_this.min), parseInt(_this.max)];

// 교차되지 않게, 완전히 겹치기보다는 어느 정도 간격을 남겨두기 위해.
_this.value = Math.min(parseInt(_this.value), parseInt(inputRight.value) - 10000);

// input, thumb 같이 움직이도록
const percent = ((_this.value - min) / (max - min)) * 100;
thumbLeft.style.left = percent + "%";
range.style.left = percent + "%";
};

const setRightValue = () => {
const _this = inputRight;
const [min, max] = [parseInt(_this.min), parseInt(_this.max)];

// 교차되지 않게, 완전히 겹치기보다는 어느 정도 간격을 남겨두기 위해.
_this.value = Math.max(parseInt(_this.value), parseInt(inputLeft.value) + 10000);

// input, thumb 같이 움직이도록
const percent = ((_this.value - min) / (max - min)) * 100;
thumbRight.style.right = 100 - percent + "%";
range.style.right = 100 - percent + "%";
};

inputLeft.addEventListener("input", setLeftValue);
inputRight.addEventListener("input", setRightValue);

// cnt값 변화시키기
function updateLeftValue() {
    cntLeft.innerText = parseInt(this.value).toLocaleString();
}
function updateRightValue() {
    cntRight.innerText = parseInt(this.value).toLocaleString();
}

inputLeft.addEventListener("change", updateLeftValue);
inputRight.addEventListener("change", updateRightValue);