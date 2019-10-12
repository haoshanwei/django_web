"""web_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from apitest import views
from items import views as itview
from case import views as cview
from bug import views as bview
from django.conf.urls import url, include, re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('login/', views.login),
    path('home/', views.home),
    path('logout/', views.logout),
    path('item/', itview.item),
    path('api/', cview.api),
    path('scence_api/', cview.scence_api),
    path('bug/', bview.bug),
    path('api_test_report/', views.api_test_report),
    path('periodic_task/', views.periodic_task),
    path('task_apis/', views.task_apis),
    path('search/', views.search, name='search'),
    path('task_apisteps/', views.task_apisteps),
    url(r'accounts/login/$', views.login),
    url(r'accounts/admin/$', views.login),
    url(r'accounts/periodic_task/$', views.login),
    url(r'accounts/bug/$', views.login),
    url(r'accounts/api/$', views.login),
    url(r'accounts/scence_api/$', views.login),
    url(r'accounts/item/$', views.login),
    path('apistep_manage/', cview.apistep_manage, name='apistep_manage'),
    path('do_apitest/', views.do_apitest, name='do_apitest'),
    path('do_single/', views.do_single, name='do_single'),



]
