(function ($) {
	'use strict';
	/*-----------------------------
	=== ALL ESSENTIAL FUNCTIONS ===
	------------------------------*/

	//=== 01. Main Menu
	function mainMenu() {
		var menuItems = $('.primary-menu'),
			navContainer = $('.header-navigation'),
			menuContainer = $('.site-nav-menu'),
			navToggler = $('.nav-toggler'),
			closeIcon = $('.nav-close');

		// Adds toggle button to li items that have children
		menuItems.find('li a').each(function () {
			if ($(this).next().length > 0) {
				$(this).parent('li').append('<span class="dd-trigger"><i class="fal fa-plus"></i></span>');
			}
		});

		// expands the dropdown menu on each click
		menuItems.find('li .dd-trigger').on('click', function (e) {
			e.preventDefault();
			$(this).toggleClass('open').parent('li').children('ul').stop(true, true).slideToggle(350);
			$(this).find("i").toggleClass("fa-minus fa-plus");
		});

		// Open menu on toggler click
		navToggler.on('click', function (e) {
			menuContainer.toggleClass('menu-opened');
			e.preventDefault();
			$(this).toggleClass('menu-opened');
		});

		// Close menu on toggler click
		closeIcon.on('click', function (e) {
			menuContainer.removeClass('menu-opened');
			navToggler.removeClass('menu-opened');
			e.preventDefault();
		});

		// check browser width in real-time
		function breakpointCheck() {
			var windoWidth = window.innerWidth;

			if (windoWidth <= 991) {
				navContainer.addClass('breakpoint-on');
			} else {
				navContainer.removeClass('breakpoint-on');
			}
		}

		breakpointCheck();
		$(window).on('resize', function () {
			breakpointCheck();
		});

		// Search Widget
		var searchBtn = $('.search-icon'),
			searchClose = $('.search-close'),
			searchFrom = $('.search-form');

		searchBtn.on('click', function (e) {
			searchFrom.toggleClass('opened');
			e.preventDefault();
		});

		searchClose.on('click', function (e) {
			searchFrom.removeClass('opened');
			e.preventDefault();
		});

		// One Page Active Class
		var scrollLink = $(".onepage-nav li a");
		$(window).scroll(function () {
			var scrollbarLocation = $(this).scrollTop();
			scrollLink.each(function () {
				var sectionOffset = $(this.hash).offset().top - 90;
				if (sectionOffset <= scrollbarLocation) {
					$(this).parent().addClass("current");
					$(this).parent().siblings().removeClass("current");
				}
			});
		});

		// One Page Nav animation
		$('a[href*="#"]').not('[href="#"]').not('[href="#0"]').click(function (event) {
			if ( !$(this).closest('.nav-item').length ) {
				if (
					location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') &&
					location.hostname == this.hostname
				) {
					var target = $(this.hash);
					target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
	
					if (target.length) {
	
						event.preventDefault();
						$('html, body').animate({
							scrollTop: target.offset().top
						}, 1000, function () {
	
							var $target = $(target);
							$target.focus();
	
							if ($target.is(":focus")) {
								return false;
							} else {
								$target.attr('tabindex', '-1');
								$target.focus();
							};
						});
					}
				}
			}
			
		});
	}

	//=== 02. Preloader
	function preloader() {
		if ($('#preloader').length) {
			$('#preloader').delay(300).fadeOut(500);
		}
	}
 
	/* niceSelect */
	$("select").niceSelect();

	/* Magnific Popup Activation Probucket */
	$(".popup").magnificPopup({
		type: "video",
	});

	  /*------------------------------
            Input Increase
        -------------------------------*/

        var minVal = 1, maxVal = 20;
        $(".increaseQty").on('click', function(){
                var $parentElm = $(this).parents(".qtySelector");
                $(this).addClass("clicked");
                setTimeout(function(){
                    $(".clicked").removeClass("clicked");
                },100);
                var value = $parentElm.find(".qtyValue").val();
                if (value < maxVal) {
                    value++;
                }
                $parentElm.find(".qtyValue").val(value);
        });
        
        $(".decreaseQty").on('click', function(){
            var $parentElm = $(this).parents(".qtySelector");
            $(this).addClass("clicked");
            setTimeout(function(){
                $(".clicked").removeClass("clicked");
            },100);
            var value = $parentElm.find(".qtyValue").val();
            if (value > 1) {
                value--;
            }
            $parentElm.find(".qtyValue").val(value);
        });

	/*  Partner Slider */
	var $totalpartner = $(".totalpartner");
	$totalpartner.owlCarousel({
		loop: true,
		nav: false,
		dots: false,
		autoplay: true,
		margin: 20,
		autoplayTimeout: 3000,
		smartSpeed: 1200,
		responsive: {
			0: {
				items: 1
			},
			360: {
				items: 2
			},
			768: {
				items: 3
			},
			992: {
				items: 3
			},
			1199: {
				items: 3
			},
			1200: {
				items: 5
			}
		}
	});

	/*  Featured Itam Slider */
	var $totalfetaure = $(".totalfetaure");
	$totalfetaure.owlCarousel({
		loop: true,
		nav: false,
		dots: false,
		autoplay: true,
		autoplayTimeout: 3000,
		smartSpeed: 1200,
		margin: 40,
		responsive: {
			0: {
				items: 1
			},
			576: {
				items: 1
			},
			768: {
				items: 2
			},
			992: {
				items: 2
			},
			1199: {
				items: 3
			},
			1400: {
				items: 4
			}
		}
	});


	/*  Testomonial Slider  index-2.html*/
	var $testotwo = $(".testotwo");
	$testotwo.owlCarousel({
		loop: true,
		dots: false,
		autoplayTimeout: 3000,
		smartSpeed: 1200,
		autoplay: true,
		nav: true,
		navText: [
			'<i class="fas fa-arrow-left"></i>',
			'<i class="fas fa-arrow-right"></i>',
		],
		margin: 0,
		responsive: {
			0: {
				items: 1
			},
			576: {
				items: 1
			},
			768: {
				items: 1
			},
			992: {
				items: 1
			},

			1200: {
				items: 2
			}

		}
	});

	/*  Banner slider index-3.html */
	var $heroarea = $(".heroarea");
	$heroarea.owlCarousel({
		loop: true,
		nav: true,
		navText: [
			'<i class="fas fa-chevron-left"></i>',
			'<i class="fas fa-chevron-right"></i>',
		],
		dots: false,
		autoplayTimeout: 3000,
		smartSpeed: 1200,
		autoplay: false,
		items: 1
	});

	/* testimonial-slider */
	var $testo = $(".testo-box");
	$testo.owlCarousel({
		loop: true,
		nav: true,
		navText: [
			'<i class="fa fa-angle-left"></i>',
			'<i class="fa fa-angle-right"></i>',
		],
		dots: true,
		animateOut: 'fadeOut',
		animateIn: 'fadeIn',
		autoplayTimeout: 4000,
		smartSpeed: 1200,
		autoplay: true,
		items: 1
	});

	/*  Testomonial Slider  index.html */
	var $testobox = $(".testobox");
	$testobox.owlCarousel({
		loop: true,
		nav: false,
		dots: false,
		autoplayTimeout: 3000,
		smartSpeed: 1200,
		autoplay: true,
		margin: 10,
		items: 1
	});

	/*  Testomonial Slider  index-3.html*/
	var $testothree = $(".testothree");
	$testothree.owlCarousel({
		loop: true,
		dots: false,
		autoplayTimeout: 3000,
		smartSpeed: 1200,
		autoplay: true,
		nav: true,
		navText: [
			'<i class="fas fa-arrow-left"></i>',
			'<i class="fas fa-arrow-right"></i>',
		],
		margin: 0,

		responsive: {
			0: {
				items: 1
			},
			576: {
				items: 1
			},
			768: {
				items: 1
			},
			992: {
				items: 2
			},

			1200: {
				items: 3
			}

		}
	});

	//=== 07. Back to top
	function showBackToTop() {
		var scroll = $(window).scrollTop();

		if (scroll > 600) {
			$('.back-to-top').fadeIn(200)
		} else {
			$('.back-to-top').fadeOut(200)
		}
	}

	function backToTop() {
		$('.back-to-top').on('click', function (e) {
			e.preventDefault();

			$('html, body').animate({
				scrollTop: 0,
			}, 1500);
		});
	}

	//=== 12. Video Popup
	function videoPopup() {
		$('.video-popup').magnificPopup({
			type: 'iframe'
		});
	}

	//===== 13. Product quantity
	function productQuantity() {
		$('.add').click(function () {
			if ($(this).prev().val()) {
				$(this).prev().val(+$(this).prev().val() + 1);
			}
		});
		$('.sub').click(function () {
			if ($(this).next().val() > 1) {
				if ($(this).next().val() > 1) $(this).next().val(+$(this).next().val() - 1);
			}
		});
	}

	//===== 15. Sticky Header
	function stickyHeader() {
		var sticky = $('header.sticky-header');
		var scrollFromtop = $(window).scrollTop();
		var scrollLimit = $('header').height() + 10;

		if (scrollFromtop < scrollLimit) {
			sticky.removeClass('sticky-on');
		} else {
			sticky.addClass('sticky-on');
		}
	}

	/*---------------------
	=== DOCUMENT READY  ===
	----------------------*/
	$(document).ready(function () {
		mainMenu();
		backToTop();
		videoPopup();
	});

	/*--------------------
	=== WINDOW SCROLL  ===
	----------------------*/
	$(window).on('scroll', function () {
		showBackToTop();
		stickyHeader();
	});

	/*------------------
	=== WINDOW LOAD  ===
	--------------------*/
	$(window).on('load', function () {
		preloader();

		new WOW().init();
	});

})(jQuery);