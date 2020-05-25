from django.urls import path, include
from . import views

app_name = "analytics_api"

urlpatterns = [
    path('get_pl_data/',views.get_pl_details, name='get_pl_details'),
    path('get_avg_tranfer/',views.get_avg_tranfer, name='get_avg_tranfer'),
]
