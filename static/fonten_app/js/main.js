(function($) {
    "use strict";

    $(document).ready(function() {

        // NivoSlider
        if ($('#mainSlider').length) {
            $('#mainSlider').nivoSlider({
                effect: 'random',
                slices: 15,
                boxCols: 8,
                boxRows: 4,
                animSpeed: 500,
                pauseTime: 4000,
                directionNav: true,
                controlNav: true,
                controlNavThumbs: false,
                pauseOnHover: true,
                manualAdvance: false,
                prevText: '<',
                nextText: '>',
                randomStart: false,
            });
        }

        // Best Sale FlexSlider
        $('#best-sale-slider').flexslider({
            animation: "slide",
            animationLoop: true,
            itemWidth: 250,
            itemMargin: 0,
            minItems: 1,
            maxItems: 1,
            controlNav: false,
            directionNav: false,
            slideshow: true,
            slideshowSpeed: 3000,
        });

        // FlexSlider for product sliders
        $('.product-flexslider').flexslider({
            animation: "slide",
            animationLoop: true,
            itemWidth: 250,
            itemMargin: 0,
            minItems: 1,
            maxItems: 1,
            controlNav: false,
            directionNav: false,
            slideshow: true,
            slideshowSpeed: 3000,
        });

        // Mean Menu (mobile)
        if ($('.mobile-menu nav').length) {
            $('.mobile-menu nav').meanmenu({
                meanScreenWidth: 991,
                meanMenuContainer: '.mobile-menu',
                meanMenuClose: '<span>X</span>',
                meanMenuCloseSize: '18px',
            });
        }

        // Owl Carousel for clients
        if ($('#our-clients-slider .slider-items').length) {
            $('#our-clients-slider .slider-items').owlCarousel({
                items: 6,
                itemsDesktop: [1199, 5],
                itemsDesktopSmall: [991, 4],
                itemsTablet: [768, 3],
                itemsMobile: [479, 2],
                navigation: false,
                pagination: false,
                slideSpeed: 1000,
                autoPlay: 3000,
            });
        }

        // WOW animations
        if (typeof WOW !== 'undefined') {
            new WOW().init();
        }

        // Back to top
        $('#back-to-top').on('click', function(e) {
            e.preventDefault();
            $('html, body').animate({ scrollTop: 0 }, 500);
        });

        // Login modal toggle
        $('[data-toggle="modal"]').on('click', function(e) {
            e.preventDefault();
            var target = $(this).data('target');
            $(target).addClass('show');
        });
        $('.modal .close, .modal').on('click', function(e) {
            if ($(e.target).hasClass('modal') || $(e.target).hasClass('close') || $(e.target).closest('.close').length) {
                $('.modal').removeClass('show');
            }
        });

        // Product hover image swap
        $('.product-image-photo').each(function() {
            var origSrc = $(this).attr('src');
            var hoverSrc = $(this).data('hover-src');
            if (!hoverSrc) return;
            $(this).closest('.product-item').on('mouseenter', function() {
                $(this).find('.product-image-photo').attr('src', hoverSrc);
            }).on('mouseleave', function() {
                $(this).find('.product-image-photo').attr('src', origSrc);
            });
        });

        // Auto-dismiss alerts
        $('.alert').delay(5000).fadeOut(500);
    });

})(jQuery);
