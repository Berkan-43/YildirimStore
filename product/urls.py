from django.urls import path
from product.views import *
from order.views import *

urlpatterns= [
    path('category/<slug:slug>', category_products, name='category_products'),
    path('campaigns/<slug:slug>', campaigns_products, name='campaigns_products'),
    path('campaigns_detail/<int:id>/<slug:slug>', campaigns_detail, name='campaigns_detail'),
    path('detail/<int:id>/<slug:slug>', detail, name='detail'),
    path('addcomment/<int:id>', addcomment, name='addcomment'),
    path('comments/', comments, name='comments'),
]