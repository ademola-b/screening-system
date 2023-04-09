(function ($) {
    if ($.fn.owlCarousel) {
        var documentSlides = $('');
        documentSlides.owlCarousel({
            
        });
    }

    if ($.fn.imagesLoaded) {
        $('.row').imagesLoaded(function () {
            // filter items on button click
            $('.portfolio-filter').on('click', 'button', function () {
                var filterValue = $(this).attr('data-filter');
                $grid.isotope({
                    filter: filterValue
                });
            });
            // init Isotope
            var $grid = $('.alazea-portfolio').isotope({
                itemSelector: '.single_portfolio_item',
                percentPosition: true,
                masonry: {
                    columnWidth: '.single_portfolio_item'
                }
            });
        });
    }
})(jQuery);