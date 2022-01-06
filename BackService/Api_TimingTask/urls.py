from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectCaseData', views.select_case_data, name='SelectCaseData'),
]
