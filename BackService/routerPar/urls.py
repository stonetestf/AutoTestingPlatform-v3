from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectData', views.select_data, name='SelectData'),
    url(r'GetPreviewData', views.get_preview_data, name='GetPreviewData'),
]
