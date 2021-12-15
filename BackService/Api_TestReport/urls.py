from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectData', views.select_data, name='SelectData'),
    # url(r'SaveData', views.save_data, name='SaveData'),
    # url(r'EditData', views.edit_data, name='EditData'),
    url(r'DeleteData', views.delete_data, name='DeleteData'),
    url(r'loadReportData', views.load_report_data, name='loadReportData'),
    # url(r'SelectHistory', views.select_history, name='SelectHistory'),
    # url(r'RestorData', views.restor_data, name='RestorData'),
]
