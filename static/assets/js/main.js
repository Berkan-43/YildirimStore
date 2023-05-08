$(document).ready(function(){"use strict";function e(){$.fn.inputSpinner&&$("input[type='number']").inputSpinner({decrementButton:'',incrementButton:'',groupClass:"input-spinner",buttonsClass:"btn-spinner",buttonsWidth:"26px"})}function t(e,t){if($.fn.owlCarousel){var o={items:1,loop:!0,margin:0,responsiveClass:!0,nav:!0,navText:['',''],dots:!0,smartSpeed:400,autoplay:!1,autoplayTimeout:15e3};void 0===e&&(e=$("body")),t&&(o=$.extend({},o,t)),e.find('[data-toggle="owl"]').each(function(){var e=$(this),t=$.extend({},o,e.data("owl-options"));e.owlCarousel(t)})}}function o(e,t){$(e).each(function(){var e=$(this);e.isotope({itemSelector:t,layoutMode:e.data("layout")?e.data("layout"):"masonry"})})}function n(e,t){$(e).find("a").on("click",function(o){var n=$(this),i=n.attr("data-filter");$(e).find(".active").removeClass("active"),$(t).isotope({filter:i,transitionDuration:"0.7s"}),n.closest("li").addClass("active"),o.preventDefault()})}t(),e();var i=$(".header-search-wrapper"),a=$("body"),s=$(".search-toggle");s.on("click",function(e){i.toggleClass("show"),$(this).toggleClass("active"),i.find("input").focus(),e.preventDefault()}),a.on("click",function(){i.hasClass("show")&&(i.removeClass("show"),s.removeClass("active"),a.removeClass("is-search-active"))}),$(".header-search").on("click",function(e){e.stopPropagation()});var r=$(".category-dropdown"),c=r.data("visible");if($(".sticky-header").length&&$(window).width()>=992){new Waypoint.Sticky({element:$(".sticky-header")[0],stuckClass:"fixed",offset:-300,handler:function(e){return c&&"up"==e?(r.addClass("show").find(".dropdown-menu").addClass("show"),r.find(".dropdown-toggle").attr("aria-expanded","true"),!1):void(r.hasClass("show")&&(r.removeClass("show").find(".dropdown-menu").removeClass("show"),r.find(".dropdown-toggle").attr("aria-expanded","false")))}})}$(".mobile-menu-toggler").on("click",function(e){a.toggleClass("mmenu-active"),$(this).toggleClass("active"),e.preventDefault()}),$(".mobile-menu-overlay, .mobile-menu-close").on("click",function(e){a.removeClass("mmenu-active"),$(".menu-toggler").removeClass("active"),e.preventDefault()}),$(".mobile-menu").find("li").each(function(){var e=$(this);e.find("ul").length&&$("",{"class":"mmenu-btn"}).appendTo(e.children("a"))}),$(".mmenu-btn").on("click",function(e){var t=$(this).closest("li"),o=t.find("ul").eq(0);t.hasClass("open")?o.slideUp(300,function(){t.removeClass("open")}):o.slideDown(300,function(){t.addClass("open")}),e.stopPropagation(),e.preventDefault()});var l=$(".sidebar-toggler");if(l.on("click",function(e){a.toggleClass("sidebar-filter-active"),$(this).toggleClass("active"),e.preventDefault()}),$(".sidebar-filter-overlay").on("click",function(e){a.removeClass("sidebar-filter-active"),l.removeClass("active"),e.preventDefault()}),$(".sidebar-filter-clear").on("click",function(e){$(".sidebar-shop").find("input").prop("checked",!1),e.preventDefault()}),$.fn.magnificPopup&&$(".btn-iframe").magnificPopup({type:"iframe",removalDelay:600,preloader:!1,fixedContentPos:!1,closeBtnInside:!1}),$.fn.hoverIntent&&$(".product-3").hoverIntent(function(){var e=$(this),t=e.outerHeight()-(e.find(".product-body").outerHeight()+e.find(".product-media").outerHeight()),o=e.find(".product-footer").outerHeight()-t;e.find(".product-footer").css({visibility:"visible",transform:"translateY(0)"}),e.find(".product-body").css("transform","translateY("+-o+"px)")},function(){var e=$(this);e.find(".product-footer").css({visibility:"hidden",transform:"translateY(100%)"}),e.find(".product-body").css("transform","translateY(0)")}),"object"==typeof noUiSlider){var d=document.getElementById("price-slider");if(null==d)return;noUiSlider.create(d,{start:[0,750],connect:!0,step:50,margin:200,range:{min:0,max:1e3},tooltips:!0,format:wNumb({decimals:0,prefix:"$"})}),d.noUiSlider.on("update",function(e){$("#filter-price-range").text(e.join(" - "))})}if($.fn.countdown&&$(".product-countdown").each(function(){var e,t=$(this),o=t.data("until"),n=t.data("compact"),i=t.data("format")?t.data("format"):"DHMS",a=t.data("labels-short")?["Years","Months","Weeks","Days","Hours","Mins","Secs"]:["Years","Months","Weeks","Days","Hours","Minutes","Seconds"],s=t.data("labels-short")?["Year","Month","Week","Day","Hour","Min","Sec"]:["Year","Month","Week","Day","Hour","Minute","Second"];if(t.data("relative"))e=o;else var r=o.split(", "),e=new Date(r[0],r[1]-1,r[2]);t.countdown({until:e,format:i,padZeroes:!0,compact:n,compactLabels:["y","m","w"," days,"],timeSeparator:" : ",labels:a,labels1:s})}),$.fn.stick_in_parent&&$(window).width()>=992&&$(".sticky-content").stick_in_parent({offset_top:80,inner_scrolling:!1}),$.fn.elevateZoom){$("#product-zoom").elevateZoom({gallery:"product-zoom-gallery",galleryActiveClass:"active",zoomType:"inner",cursor:"crosshair",zoomWindowFadeIn:400,zoomWindowFadeOut:400,responsive:!0}),$(".product-gallery-item").on("click",function(e){$("#product-zoom-gallery").find("a").removeClass("active"),$(this).addClass("active"),e.preventDefault()});var u=$("#product-zoom").data("elevateZoom");$("#btn-product-gallery").on("click",function(e){$.fn.magnificPopup&&($.magnificPopup.open({items:u.getGalleryList(),type:"image",gallery:{enabled:!0},fixedContentPos:!1,removalDelay:600,closeBtnInside:!1},0),e.preventDefault())})}if($.fn.owlCarousel&&$.fn.elevateZoom){var f=$(".product-gallery-carousel");f.on("initialized.owl.carousel",function(){f.find(".active img").elevateZoom({zoomType:"inner",cursor:"crosshair",zoomWindowFadeIn:400,zoomWindowFadeOut:400,responsive:!0})}),f.owlCarousel({loop:!1,margin:0,responsiveClass:!0,nav:!0,navText:['',''],dots:!1,smartSpeed:400,autoplay:!1,autoplayTimeout:15e3,responsive:{0:{items:1},560:{items:2},992:{items:3},1200:{items:3}}}),f.on("change.owl.carousel",function(){$(".zoomContainer").remove()}),f.on("translated.owl.carousel",function(){f.find(".active img").elevateZoom({zoomType:"inner",cursor:"crosshair",zoomWindowFadeIn:400,zoomWindowFadeOut:400,responsive:!0})})}if($.fn.elevateZoom){$(".product-separated-item").find("img").elevateZoom({zoomType:"inner",cursor:"crosshair",zoomWindowFadeIn:400,zoomWindowFadeOut:400,responsive:!0});var p=[];$(".product-gallery-separated").find("img").each(function(){var e=$(this),t=e.attr("src"),o=e.attr("alt"),n={src:t,title:o};p.push(n)}),$("#btn-separated-gallery").on("click",function(e){$.fn.magnificPopup&&($.magnificPopup.open({items:p,type:"image",gallery:{enabled:!0},fixedContentPos:!1,removalDelay:600,closeBtnInside:!1},0),e.preventDefault())})}$("#checkout-discount-input").on("focus",function(){$(this).parent("form").find("label").css("opacity",0)}).on("blur",function(){var e=$(this);0!==e.val().length?e.parent("form").find("label").css("opacity",0):e.parent("form").find("label").css("opacity",1)}),$(".tab-trigger-link").on("click",function(e){var t=$(this).attr("href");$(".nav-dashboard").find('a[href="'+t+'"]').trigger("click"),e.preventDefault()}),"function"==typeof imagesLoaded&&$.fn.isotope&&($(".portfolio-container").imagesLoaded(function(){o(".portfolio-container",".portfolio-item"),n(".portfolio-filter",".portfolio-container")}),$(".entry-container").imagesLoaded(function(){o(".entry-container",".entry-item"),n(".entry-filter",".entry-container")}),$(".product-gallery-masonry").imagesLoaded(function(){o(".product-gallery-masonry",".product-gallery-item")}),$(".products-container").imagesLoaded(function(){o(".products-container",".product-item"),n(".product-filter",".products-container")}));var m=$(".count");$.fn.countTo?$.fn.waypoint?m.waypoint(function(){$(this.element).countTo()},{offset:"90%",triggerOnce:!0}):m.countTo():m.each(function(){var e=$(this),t=e.data("to");e.text(t)});var v=$(".scroll-to");v.length&&v.on("click",function(e){var t=$(this).attr("href"),o=$(t);if(o.length){var n=$(window).width()<992?o.offset().top:o.offset().top-52;$("html, body").animate({scrollTop:n},600),e.preventDefault()}}),$("#review-link").on("click",function(e){var t=$(this).attr("href"),o=$(t);if($("#product-accordion-review").length&&$("#product-accordion-review").collapse("show"),o.length){var n=$(window).width()<992?o.offset().top-10:o.offset().top-72;$("html, body").animate({scrollTop:n},600),o.tab("show")}e.preventDefault()});var g=$("#scroll-top");if($(window).on("load scroll",function(){$(window).scrollTop()<400?g.removeClass("show"):g.addClass("show")}),g.on("click",function(e){$("html, body").animate({scrollTop:0},800),e.preventDefault()}),document.getElementById("map")&&"object"==typeof google){var h,y='88 Pine St,New York, NY 10005, USAGet Directions ',w=new google.maps.LatLng(40.8127911,-73.9624553),b=new google.maps.Map(document.getElementById("map"),{zoom:14,center:w,scrollwheel:!1,mapTypeId:google.maps.MapTypeId.ROADMAP}),k=new google.maps.InfoWindow({content:y,maxWidth:360});h=new google.maps.Marker({position:w,map:b,animation:google.maps.Animation.DROP}),google.maps.event.addListener(h,"click",function(e){return function(){k.open(b,e)}}(h))}var C=$(".view-all-demos");C.on("click",function(e){e.preventDefault(),$(".demo-item.hidden").addClass("show"),$(this).addClass("disabled-hidden")}),$(".btn-quickview").on("click",function(o){var n=$(this).attr("href");$.fn.magnificPopup&&(setTimeout(function(){$.magnificPopup.open({type:"ajax",mainClass:"mfp-ajax-product",tLoading:"",preloader:!1,removalDelay:350,items:{src:n},callbacks:{ajaxContentAdded:function(){t($(".quickView-content"),{onTranslate:function(e){var t=$(e.target),o=(t.data("owl.carousel").current()+e.item.count-Math.ceil(e.item.count/2))%e.item.count;$(".quickView-content .carousel-dot").eq(o).addClass("active").siblings().removeClass("active")}}),e()},open:function(){$("body").css("overflow-x","visible"),$(".sticky-header.fixed").css("padding-right","1.7rem")},close:function(){$("body").css("overflow-x","hidden"),$(".sticky-header.fixed").css("padding-right","0")}},ajax:{tError:""}},0)},500),o.preventDefault())}),$("body").on("click",".carousel-dot",function(){$(this).siblings().removeClass("active"),$(this).addClass("active")}),$("body").on("click",".btn-fullscreen",function(o){var n=[];$(this).parents(".owl-stage-outer").find(".owl-item:not(.cloned)").each(function(){var e=$(this).find("img"),t=e.attr("src"),o=e.attr("alt"),i={src:t,title:o};n.push(i)});var i=$(this).attr("href"),a=$.magnificPopup.instance;a.isOpen&&a.close(),setTimeout(function(){$.magnificPopup.open({type:"ajax",mainClass:"mfp-ajax-product",tLoading:"",preloader:!1,removalDelay:350,items:{src:i},callbacks:{ajaxContentAdded:function(){t($(".quickView-content"),{onTranslate:function(e){var t=$(e.target),o=(t.data("owl.carousel").current()+e.item.count-Math.ceil(e.item.count/2))%e.item.count;$(".quickView-content .carousel-dot").eq(o).addClass("active").siblings().removeClass("active"),$(".curidx").html(o+1)}}),e()},open:function(){$("body").css("overflow-x","visible"),$(".sticky-header.fixed").css("padding-right","1.7rem")},close:function(){$("body").css("overflow-x","hidden"),$(".sticky-header.fixed").css("padding-right","0")}},ajax:{tError:""}},0)},500),o.preventDefault()}),document.getElementById("newsletter-popup-form")&&setTimeout(function(){var e=$.magnificPopup.instance;e.isOpen&&e.close(),setTimeout(function(){$.magnificPopup.open({items:{src:"#newsletter-popup-form"},type:"inline",removalDelay:350,callbacks:{open:function(){$("body").css("overflow-x","visible"),$(".sticky-header.fixed").css("padding-right","1.7rem")},close:function(){$("body").css("overflow-x","hidden"),$(".sticky-header.fixed").css("padding-right","0")}}})},500)},1e4)});