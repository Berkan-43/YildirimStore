from django.urls import path
from user.views import *
from django.contrib.auth import views as auth_views
from . import views
from allauth.account.views import LoginView, SignupView 
from user.views import MyOrdersView, OrderDetailView

urlpatterns = [
    path('update/', user_update, name='user_update'),
    path("sepetim/",views.v_cart,name="shoppingcart"),
    path("favorilerim/",views.v_favorites,name="favories"),
    path("profile/",views.v_profile,name="profile"),
    path("userDelete/",userDelete,name="userdelete"),
    path("adressDelete/",adressDelete,name="adressDelete"),
    path("update_item/",views.f_update_item,name="update_item"),
    path("update-cart/",views.f_update_cart,name="update-cart"),
    path("update-favorites/",views.f_update_favorites,name="update-favorites"),
    path('customurl/login/', LoginView.as_view(), name="account_login" ),
    path('customurl/signup/', SignupView.as_view(), name="account_singup" ),
    path("my-orders/",MyOrdersView.as_view(),name="url_myOrders"),
    path("order-detail/<str:order_number>",OrderDetailView.as_view(),name="url_orderDetail"),
    path('deleteformfavories/<int:id>', deleteformfavories, name='deleteformfavories'),
]