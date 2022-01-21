from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectData', views.select_data, name='SelectData'),
    url(r'SaveData', views.save_data, name='SaveData'),
    url(r'EditData', views.edit_data, name='EditData'),
    url(r'DeleteData', views.delete_data, name='DeleteData'),
    url(r'CharmEventData', views.charm_event_data, name='CharmEventData'),
    url(r'LoadData', views.load_data, name='LoadData'),
    # url(r'DeleteMembers', views.delete_members, name='DeleteMembers'),
    # url(r'VerifyEnterInto', views.verify_enter_into, name='VerifyEnterInto'),
    # url(r'SelectHistory', views.select_history, name='SelectHistory'),
    # url(r'RestorData', views.restor_data, name='RestorData'),
]
