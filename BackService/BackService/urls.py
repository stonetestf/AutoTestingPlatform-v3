"""BackService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.urls import path
from django.conf.urls import url, include

import login.urls
import home.urls
import upLoad.urls
import routerPar.urls
import role.urls

urlpatterns = [
    # path('admin/', admin.site.urls),
    url('api/login/', include(login.urls)),
    url('api/home/', include(home.urls)),
    url('api/upLoad/', include(upLoad.urls)),
    url('api/router/', include(routerPar.urls)),
    url('api/role/', include(role.urls)),
]
