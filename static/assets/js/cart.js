(function(DOMParser) {
  "use strict";

  var proto = DOMParser.prototype,
      nativeParse = proto.parseFromString;

  // Firefox/Opera/IE throw errors on unsupported types
  try {
      // WebKit returns null on unsupported types
      if ((new DOMParser()).parseFromString("", "text/html")) {
          // text/html parsing is natively supported
          return;
      }
  } catch (ex) {}

  proto.parseFromString = function(markup, type) {
      if (/^\s*text\/html\s*(?:;|$)/i.test(type)) {
          var doc = document.implementation.createHTMLDocument("");
          if (markup.toLowerCase().indexOf('<!doctype') > -1) {
              doc.documentElement.innerHTML = markup;
          } else {
              doc.body.innerHTML = markup;
          }
          return doc;
      } else {
          return nativeParse.apply(this, arguments);
      }
  };
})(DOMParser);

function clickAddToCartButton(target) {
  var productId = target.dataset.product;
  var action = target.dataset.action;
  console.log("product ID:", productId, "Action: ", action);
  console.log("USER: ", user);
  if (user == "AnonymousUser") {
    console.log("Kullanıcı giriş yapmamış");
  } else {
    updateUserOrder(productId, action);
  }
}

function updateCartData() {
  var url = "/";
  fetch(url)
    .then((response) => {
      return response.text();
    })
    .then((data) => {
      var parser = new DOMParser();
      var doc = parser.parseFromString(data, "text/html");
      var cartDataContainer = doc.getElementById("data");
      var updatedCartData = cartDataContainer.innerHTML;
      
      document.getElementById("data").innerHTML = updatedCartData;
    });
}

function updateUserOrder(productId, action) {
  console.log("Giriş yapıldı ve sepete ekleniyor");
  var url = "/user/update_item/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      var message = document.createElement("div");
      document.body.appendChild(message);
      message.className = "flex items-center w-full fixed top-10 right-5  max-w-md p-4 mb-4 text-gray-500 bg-white rounded-lg shadow dark:text-gray-400 dark:bg-gray-800 productCartAdd";
      message.innerHTML = data;
      setTimeout(() => {
        message.classList.add("closing-effect");
      }, 3000);
      setTimeout(function () {
        message.remove();
      }, 4000);

      // Update cart data in navbar
      updateCartData();
    });
}

// Loading button
$(document).ajaxSend(function() {
  $(".spinner-border").fadeIn(500);
});

$(document).ajaxComplete(function() {
  $(".spinner-border").fadeOut(500);
});

$.ajaxSetup({
  headers: {
    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
  }
});

$(document).on("click", ".btn-send", function() {
  var btn = $(this);
  var btn_id = btn.attr('id');
  var loading = '<div class="spinner-border"></div>'
  btn.html(loading);

  $.ajax({
    type: 'POST',
    success: function(data) {
      console.log(data);
    },
    complete: function() {
      $(".spinner-border").fadeOut(500, function() {
        btn.html('<span>Sepete Ekle</span>');
      });
    }
  });
});

