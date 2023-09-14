// 물주기 점수차트
const wateringScore = document.getElementById('watering_score');
const wateringScoreNum = document.getElementById('watering_score_num').innerText;

const wateringValue = parseInt(wateringScoreNum) / 20 * 100; // 물주기 점수 길이 비율구하기

let wateringWidth = 0
wateringScore.style.width = 0
const wateringBarAnimation = setInterval(() => {
    wateringScore.style.width =  wateringWidth + '%'
    wateringWidth++ >= wateringValue && clearInterval(wateringBarAnimation)
}, 10)



// 일조 점수차트
const sunlightScore = document.getElementById('sunlight_score');
const sunlightScoreNum = document.getElementById('sunlight_score_num').innerText;

const sunlightValue = parseInt(sunlightScoreNum) / 20 * 100; // 일조 점수 길이 비율구하기

let sunlightWidth = 0
sunlightScore.style.width = 0
const sunlightBarAnimation = setInterval(() => {
    sunlightScore.style.width =  sunlightWidth + '%'
    sunlightWidth++ >= sunlightValue && clearInterval(sunlightBarAnimation)
}, 10)



// 습도 점수차트
const humidityScore = document.getElementById('humidity_score');
const humidityScoreNum = document.getElementById('humidity_score_num').innerText;

const humidityValue = parseInt(humidityScoreNum) / 20 * 100; // 습도 점수 길이 비율구하기

let humidityWidth = 0
humidityScore.style.width = 0
const humidityBarAnimation = setInterval(() => {
    humidityScore.style.width =  humidityWidth + '%'
    humidityWidth++ >= humidityValue && clearInterval(humidityBarAnimation)
}, 10)



// 온도 점수차트
const temperatureScore = document.getElementById('temperature_score');
const temperatureScoreNum = document.getElementById('temperature_score_num').innerText;

const temperatureValue = parseInt(temperatureScoreNum) / 20 * 100; // 일조 점수 길이 비율구하기

let temperatureWidth = 0
temperatureScore.style.width = 0
const temperatureBarAnimation = setInterval(() => {
    temperatureScore.style.width =  temperatureWidth + '%'
    temperatureWidth++ >= temperatureValue && clearInterval(temperatureBarAnimation)
}, 10)



// 영양 점수차트
const thingsScore = document.getElementById('things_score');
const thingsScoreNum = document.getElementById('things_score_num').innerText;

const thingsValue = parseInt(thingsScoreNum) / 20 * 100; // 일조 점수 길이 비율구하기

let thingsWidth = 0
thingsScore.style.width = 0
const thingsBarAnimation = setInterval(() => {
    thingsScore.style.width =  thingsWidth + '%'
    thingsWidth++ >= thingsValue && clearInterval(thingsBarAnimation)
}, 10)