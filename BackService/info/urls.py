from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectOperationalInfo', views.select_operational_info, name='SelectOperationalInfo'),
]
