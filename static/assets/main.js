jQuery(document).ready(function(t){"use strict";t(".demo-filter a").on("click",function(e){e.preventDefault();var i=t(this).attr("href").replace("#","");t(".demos").isotope({filter:"."+i}),t(this).addClass("active").siblings().removeClass("active")}),t(".molla-lz").lazyload({effect:"fadeIn",effect_speed:400,appearEffect:"",appear:function(){},load:function(){t(this).removeClass("molla-lz").css("padding-top","")}}),t(".mobile-menu-toggler").on("click",function(e){t("body").toggleClass("mmenu-active"),t(this).toggleClass("active"),e.preventDefault()}),t(".mobile-menu-overlay, .mobile-menu-close").on("click",function(e){t("body").removeClass("mmenu-active"),t(".menu-toggler").removeClass("active"),e.preventDefault()}),t(".goto-demos").on("click",function(e){e.preventDefault(),t("html, body").animate({scrollTop:t(".row.demos").offset().top},600)}),t(".goto-features").on("click",function(e){e.preventDefault(),t("html, body").animate({scrollTop:t(".section-features").offset().top},800)}),t(".goto-elements").on("click",function(e){e.preventDefault(),t("html, body").animate({scrollTop:t(".section-elements").offset().top},1e3)}),t(".goto-support").on("click",function(e){e.preventDefault(),t("html, body").animate({scrollTop:t(".section-support").offset().top},1200)})}),jQuery(window).on("load",function(){jQuery(".demos").isotope({filter:".homepages",initLayout:!0,itemSelector:".iso-item",layoutMode:"masonry"}).on("layoutComplete",function(){jQuery(window).trigger("scroll")})});