from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectData', views.select_data, name='SelectData'),
    url(r'SelectCaseData', views.select_case_data, name='SelectCaseData'),
    url(r'CharmTaskData', views.charm_task_data, name='CharmTaskData'),
    url(r'SaveData', views.save_data, name='SaveData'),
    url(r'LoadTaskData', views.load_task_data, name='LoadTaskData'),
]
