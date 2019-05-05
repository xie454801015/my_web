from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('register/check/', views.duplicate_check, name='duplicate_check'),
    path('verify_code/', views.captcha_set, name='captcha_set'),

]
