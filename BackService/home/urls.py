from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'LoadUserInfo', views.load_user_info, name='LoadUserInfo'),
    url(r'SaveUserInfo', views.save_user_info, name='SaveUserInfo'),
    url(r'GetHomePermissions', views.get_home_permissions, name='GetHomePermissions'),
    url(r'GetRouterPath', views.get_router_path, name='GetRouterPath'),
    url(r'GetUserStatisticsInfo', views.get_user_statistics_info, name='GetUserStatisticsInfo'),
]