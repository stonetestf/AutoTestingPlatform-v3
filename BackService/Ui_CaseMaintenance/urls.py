from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectData', views.select_data, name='SelectData'),
    url(r'SaveData', views.save_data, name='SaveData'),
    url(r'EditData', views.edit_data, name='EditData'),
    url(r'DeleteData', views.delete_data, name='DeleteData'),
    url(r'CharmCaseData', views.charm_case_data, name='CharmCaseData'),
    url(r'LoadCaseData', views.load_case_data, name='LoadCaseData'),
    # url(r'LoadOperationData', views.load_operation_data, name='LoadOperationData'),
    # url(r'UpdateOperationSort', views.update_operation_sort, name='UpdateOperationSort'),
    # url(r'GetElementOperationTypeItems', views.get_element_operation_type_items, name='GetElementOperationTypeItems'),
]
