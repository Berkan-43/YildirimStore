from django.urls import path
from .views import PlaceOrderView,PaymentView,OrderCompleteView, CheckoutView

urlpatterns = [
    path("place-order",PlaceOrderView.as_view(),name="url_placeOrder"),
    path("payments/",PaymentView.as_view(),name="url_payment"),
    path("order-complete/",OrderCompleteView.as_view(),name="url_orderComplete"),
    path("checkout/",CheckoutView.as_view(),name="url_checkout"),
]