from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectData', views.select_data, name='SelectData'),
    url(r'SaveData', views.save_data, name='SaveData'),
    url(r'EditData', views.edit_data, name='EditData'),
    url(r'DeleteData', views.delete_data, name='DeleteData'),
    url(r'LoadCaseData', views.load_case_data, name='LoadCaseData'),
    url(r'LoadData', views.load_data, name='LoadData'),
    url(r'CharmCaseData', views.charm_case_data, name='CharmCaseData'),
    # url(r'SendTestRequest', views.send_test_request, name='SendTestRequest'),
    # url(r'CopyApi', views.copy_api, name='CopyApi'),
    # url(r'SelectHistory', views.select_history, name='SelectHistory'),
    # url(r'RestorData', views.restor_data, name='RestorData'),

]
