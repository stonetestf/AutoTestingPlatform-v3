from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'LoadUserInfo', views.load_user_info, name='LoadUserInfo'),
    url(r'SaveUserInfo', views.save_user_info, name='SaveUserInfo'),
    url(r'GetHomePermissions', views.get_home_permissions, name='GetHomePermissions'),
    url(r'GetApiPermissions', views.get_api_permissions, name='GetApiPermissions'),
    url(r'GetRouterPath', views.get_router_path, name='GetRouterPath'),
    url(r'GetUserStatisticsInfo', views.get_user_statistics_info, name='GetUserStatisticsInfo'),
    url(r'GetServerIndicators', views.get_server_indicators, name='GetServerIndicators'),
    url(r'ApiPageHomeSelectTestResults', views.api_pagehome_select_test_results, name='ApiPageHomeSelectTestResults'),
]