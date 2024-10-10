from django.urls import path
from . import views
from .views import Checklogin, registerAction, CheckloginAjaxs
from django.contrib.auth import views as auth_views


urlpatterns=[

    path('register', views.register, name="home"),
    path('logins', views.logins, name="logins"),
    path('Checklogin', views.Checklogin, name="Checklogin"),
    path('registerAction', views.registerAction, name="registerAction"),
    path('CheckAuth', views.CheckAuth, name="CheckAuth"),
    path('LogOut', views.LogOut, name="LogOut"),
    path('CheckloginAjaxs/<str:UserName>/<str:Password>', views.CheckloginAjaxs, name="CheckloginAjaxs"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

]

