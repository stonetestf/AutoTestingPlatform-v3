from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectData', views.select_data, name='SelectData'),
    url(r'SaveData', views.save_data, name='SaveData'),
    url(r'EditData', views.edit_data, name='EditData'),
    url(r'DeleteData', views.delete_data, name='DeleteData'),
    url(r'CharmApiData', views.charm_api_data, name='CharmApiData'),
    url(r'LoadData', views.load_data, name='LoadData'),
    url(r'SendRequest', views.send_request, name='SendRequest'),
    url(r'CopyApi', views.copy_api, name='CopyApi'),

]
