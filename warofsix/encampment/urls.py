from django.urls import path
from . import views

app_name = "encampment"

urlpatterns = [
    path('', views.EncampmentListView.as_view(), name="encampment"),
    
]
