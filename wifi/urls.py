from django.urls import path
from . import views
app_name = 'wifi'
urlpatterns = [
    path('', views.index, name='index'),
    path('data/<int:device_id>', views.router_data_update, name='data'),

]
