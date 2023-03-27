from django.urls import path
from . import views

app_name="battle"

urlpatterns = [
    path('', views.battle_view, name="battle"),
    path('report/<int:pk>/', views.BattleReportDetailView.as_view(), name="report"),
    
]
