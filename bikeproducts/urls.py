from django.urls import path
from . import views

urlpatterns=[
    path('index.html', views.home, name="Home"),
    path('about.html', views.about, name="About us"),
    path('about.html', views.about, name="About"),
    path('contact.html', views.contact, name="Contact us"),
    path('contact.html', views.contact, name="Contact"),
    path('shop.html', views.shop, name="Shop"),
    path('shop-single.html', views.shop, name="Shop single"),
    path('view/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('panel/', views.panel, name='panel'),
    path('payment/', views.payment, name='payment'),

]
