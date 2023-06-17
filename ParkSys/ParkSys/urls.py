from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    # for test
    path('m_test/', views.m_test, name='m_test'),
    path('m_map/', views.m_map, name='m_map'),

    # for practice
    path('', views.homepage, name='homepage'),
    path('map/', views.map, name='map'),
    path('charge/', views.charge, name='charge'),
    path('contact/', views.contact, name='contact'),
    path('admin/', views.admin, name='admin'),
    path('admin0/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('showstallstatus/', views.showstallstatus, name='showstallstatus'),
    path('parkin/', views.parkin, name='parkin'),
    path('get_stakestatus/', views.get_stakestatus, name='get_stakestatus'),
    path('recognize/', views.recognize, name='recognize'),
    path('parkout/', views.parkout, name='parkout'),

]
