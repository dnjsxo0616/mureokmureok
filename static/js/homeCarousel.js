$('.slider-1 > .owl-carousel').owlCarousel({
    autoplay:true, // 오토 플레이
    autoplayTimeout:6000, // 오토 플레이 시에 다음 슬라이드로 넘어가는 주기, 2초
    loop:true,
    margin:0,
    nav:true,
    navText:['<img src="http://www.inavi.com/Content2/Images/main/icon-prev.png">', '<img src="http://www.inavi.com/Content2/Images/main/icon-next.png">'],
    responsive:{
        0:{
            items:1
        }
    }
});

var $firstDot = $('.slider-1 > .owl-carousel > .owl-dots > .owl-dot.active');

$firstDot.removeClass('active');

setTimeout(function() {
    $firstDot.addClass('active');
}, 100);