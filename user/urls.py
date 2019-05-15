from django.urls import path

from user.views import *

app_name='user'
urlpatterns = [
    path('register',user_register,name='register'),
    path('login',user_login,name='login'),
    path('codelogin',code_login,name='codelogin'),
    path('sendcode',send_code,name='sendcode'),
    path('logout',user_logout,name='logout'),
    path('forget_pwd',forget_password,name='forget_pwd'),
    path('valide_code',valide_code,name='valide_code'),
    path('update_pwd',update_pwd,name='update_pwd'),
    path('center',user_center,name='center'), #本地存储
    path('center1',user_center1,name='center1'), #云存储
    path('about',user_about,name='about'),


]