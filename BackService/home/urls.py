from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'LoadUserInfo', views.load_user_info, name='LoadUserInfo'),
    url(r'SaveUserInfo', views.save_user_info, name='SaveUserInfo'),
]