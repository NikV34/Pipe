from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'input-data-geometry\/(?P<project_id>\d+)', views.input_data_geometry, name='input-geometry'),
    re_path(r'input-data-thermal\/(?P<project_id>\d+)', views.input_data_thermal, name='input-thermal'),
    re_path(r'result-thermal\/(?P<project_id>\d+)/(?P<volume_gas>\d+)/(?P<current_temperature_gas>\d+)/(?P<current_temperature>(|.)\d+)', views.result_thermal, name='result-thermal')
]
