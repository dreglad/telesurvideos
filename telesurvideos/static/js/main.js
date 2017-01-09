
	'use strict';


	var isMobile = {
		Android: function() {
			return navigator.userAgent.match(/Android/i);
		},
		BlackBerry: function() {
			return navigator.userAgent.match(/BlackBerry/i);
		},
		iOS: function() {
			return navigator.userAgent.match(/iPhone|iPad|iPod/i);
		},
		Opera: function() {
			return navigator.userAgent.match(/Opera Mini/i);
		},
		Windows: function() {
			return navigator.userAgent.match(/IEMobile/i);
		},
		any: function() {
			return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
		}
	};


	var mobileMenuOutsideClick = function() {

		$(document).click(function (e) {
			var container = $("#gtco-offcanvas, .js-gtco-nav-toggle");
			if (!container.is(e.target) && container.has(e.target).length === 0) {

				if ( $('body').hasClass('offcanvas') ) {

					$('body').removeClass('offcanvas');
					$('.js-gtco-nav-toggle').removeClass('active');

				}


			}
		});

	};


	var scrollNavBar = function() {

		if ( $(window).scrollTop() > 50)  {
			$('body').addClass('scrolled');
			$('.js-gtco-nav-toggle').removeClass('gtco-nav-white');
		} else {
			$('body').removeClass('scrolled');
			$('.js-gtco-nav-toggle').addClass('gtco-nav-white');
		}

		$(window).scroll(function(){
			if ( $(window).scrollTop() > 50)  {
				$('body').addClass('scrolled');
				$('.gtco-nav .search input').removeClass('extended');
				$('.js-gtco-nav-toggle').removeClass('gtco-nav-white');
			} else {
				$('body').removeClass('scrolled');
				if($('.gtco-nav .search input').val().length>0)
					$('.gtco-nav .search input').addClass('extended');
				$('.js-gtco-nav-toggle').addClass('gtco-nav-white');
			}
		});


	};

	var offcanvasMenu = function() {

		$('#page').prepend('<div id="gtco-offcanvas" />');
		$('#page').prepend('<a href="#" class="js-gtco-nav-toggle gtco-nav-toggle gtco-nav-white"><i></i></a>');
		var logo = $('#gtco-logo').clone();
		$('#gtco-offcanvas').append(logo);
		var clone1 = $('.menu-1 > ul').clone();
		$('#gtco-offcanvas').append(clone1);
		var search_clone = $('.gtco-nav .search').clone();
		$('#gtco-offcanvas').append(search_clone);
		var clone2 = $('.menu-2 > ul').clone();
		$('#gtco-offcanvas').append(clone2);

		$('#gtco-offcanvas .has-dropdown').addClass('offcanvas-has-dropdown');
		$('#gtco-offcanvas')
			.find('li')
			.removeClass('has-dropdown');

		// Hover dropdown menu on mobile
		$('.offcanvas-has-dropdown').mouseenter(function(){
			var $this = $(this);

			$this
				.addClass('active')
				.find('ul')
				.slideDown(500, 'easeOutExpo');
		}).mouseleave(function(){

			var $this = $(this);
			$this
				.removeClass('active')
				.find('ul')
				.slideUp(500, 'easeOutExpo');
		});


		$(window).resize(function(){

			if ( $('body').hasClass('offcanvas') ) {

				$('body').removeClass('offcanvas');
				$('.js-gtco-nav-toggle').removeClass('active');

			}
		});
	};


	var burgerMenu = function() {

		$('body').on('click', '.js-gtco-nav-toggle', function(event){
			var $this = $(this);


			if ( $('body').hasClass('overflow offcanvas') ) {
				$('body').removeClass('overflow offcanvas');
			} else {
				$('body').addClass('overflow offcanvas');
			}
			$this.toggleClass('active');
			event.preventDefault();

		});
	};



	var contentWayPoint = function() {

		var i = 0;
		$('.animate-box').waypoint( function( direction ) {

			if( direction === 'down' && !$(this.element).hasClass('animated-fast') ) {

				i++;

				$(this.element).addClass('item-animate');
				setTimeout(function(){

					$('body .animate-box.item-animate').each(function(k){

						var el = $(this);
						setTimeout( function () {
							var effect = el.data('animate-effect');
							if ( effect === 'fadeIn') {
								el.addClass('fadeIn animated-fast');
							} else if ( effect === 'fadeInLeft') {
								el.addClass('fadeInLeft animated-fast');
							} else if ( effect === 'fadeInRight') {
								el.addClass('fadeInRight animated-fast');
							} else {
								el.addClass('fadeInUp animated-fast');
							}

							el.removeClass('item-animate');
						},  k * 50, 'easeInOutExpo' );
					});

				}, 100);

			}

		} , { offset: '85%' } );
	};


	var dropdown = function() {

		$('.has-dropdown').mouseenter(function(){

			var $this = $(this);
			$this
				.find('.dropdown')
				.css('display', 'block')
				.addClass('animated-fast fadeInUpMenu');

		}).mouseleave(function(){
			var $this = $(this);

			$this
				.find('.dropdown')
				.css('display', 'none')
				.removeClass('animated-fast fadeInUpMenu');
		});

	};


	var goToTop = function() {

		$('.js-gotop').on('click', function(event){

			event.preventDefault();

			$('html, body').animate({
				scrollTop: $('html').offset().top
			}, 500, 'easeInOutExpo');

			return false;
		});

		$(window).scroll(function(){

			var $win = $(window);
			if ($win.scrollTop() > 200) {
				$('.js-top').addClass('active');
			} else {
				$('.js-top').removeClass('active');
			}

		});

	};


	// Loading page
	var loaderPage = function() {
		$(".gtco-loader").fadeOut("slow");
	};

	var counter = function() {
		$('.js-counter').countTo({
			formatter: function (value, options) {
				return value.toFixed(options.decimals);
			},
		});
	};

	var counterWayPoint = function() {
		if ($('#gtco-counter').length > 0 ) {
			$('#gtco-counter').waypoint( function( direction ) {

				if( direction === 'down' && !$(this.element).hasClass('animated') ) {
					setTimeout( counter , 400);
					$(this.element).addClass('animated');
				}
			} , { offset: '90%' } );
		}
	};

	var parallax = function() {
		if ( !isMobile.any()) {
			$(window).stellar();
		}
	};


	var reset_minheight = function () {
		$(".gtco-post-list li.video").each(function( index ){
			if($(this).find('.entry-desc > p').text().length > 0)
				$(this).css('min-height','400px');

		});
	};
	var search = function(){
		$('.gtco-nav .search').on('click mouseenter mouseover', function(){
			var input = $(this).find('input');
			input.addClass('extended').focus().on('blur', function() {
				if (!input.val())
				    input.removeClass('extended');
			});
		});
	};

	$(function(){
		$(document).on('keypress', '#header-search input[name=q]', function(e){
            if (e.which == '13') {
                e.preventDefault();
                var q = $(this).val();
                location.href= $(this).attr('data-url') + (q ? '?q='+q : '');
            }
        });

		loaderPage();
		mobileMenuOutsideClick();
		scrollNavBar();
		offcanvasMenu();
		burgerMenu();
		contentWayPoint();
		dropdown();
		goToTop();

		counterWayPoint();
		parallax();
		reset_minheight();
		search();

		// Fullscreen with fixed items bugfix
		$(document).on("webkitfullscreenchange mozfullscreenchange fullscreenchange", function( event ) {
			$('nav, .cp-l, .related, #cms-top, #gtco-footer').toggle();
		});

		// List pagination
		$(document).on('click', 'div.pagination a.more', function(ev) {
		    ev.preventDefault();
		    var link = $(this);
		    link.attr('disabled', 'disabled').text('Cargando más videos...');
		    $.ajax({ url: link.attr('href') }).done(function(resp) {
		      link.parent().replaceWith(resp);
		      contentWayPoint();
		    });
		});

		// Search pagination
		$(document).on('click', '#extra-results .pagination a', function(ev) {
		    ev.preventDefault();
		    $(this).text('Cargando más resultados...');
		    $(this).attr('disabled', 'disabled');
		    $.ajax({
		      url: $.query.set('page', (parseInt($.query.get('page')) || 1) + 1).toString(),
		    }).done(function(resp) {
		      $('#extra-results').replaceWith(resp);
		      contentWayPoint();
		    });
		  });

		// Search filter lazy loaded
		$('#f_paises, #f_programas, #f_corresponsales').each(function() {
			$(this).find('img.lazy').lazyload({
				container: $(this),
				threshold: 50
			});
		});

		$('#page').on('swipe',function(ev){
			console.log('sjfnkjsnf');
			$('body').toggleClass('offcanvas');
		})

	});


