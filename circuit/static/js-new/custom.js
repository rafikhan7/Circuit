$(document).ready(function() {

    //Nav baar active 
    $(".nav-item").on("click", function(e) {
        $("li.nav-item").removeClass("active");
        $(this).addClass("active");
    });


    //Mobile Nav active 
    $(".mobile-menu a").on("click", function(e) {
        $(".mobile-menu a.d-inline-flex").removeClass("active");
        $(this).addClass("active");
    });



     //Cat active
    $(".categories a").on("click", function(e) {
        $(".categories a.cat-link").removeClass("active");
        $(this).addClass("active");
    });

    //Product Slider
    $('.customer-logos').slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        autoplay: false,
        autoplaySpeed: 1500,
        arrows: true,
        dots: false,
        pauseOnHover: true,
        responsive: [{
            breakpoint: 768,
            settings: {
                slidesToShow: 5
            }
        }, {
            breakpoint: 520,
            settings: {
                slidesToShow: 3
            }
        }]
    });
      //Slider arrow.
    $(".slick-prev.slick-arrow").removeAttr("style");
    $(".slick-next").on("click", function(e) {
        $(".slick-prev.slick-arrow").css("display","block");
    });

});