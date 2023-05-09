from django.urls import path
from . import views

app_name="battle"

urlpatterns = [
    path('', views.battle_view, name="battle"),
    path('reports', views.BattleReportListView.as_view(), name="reports"),
    path('report/<int:pk>/', views.BattleReportDetailView.as_view(), name="report"),
    
]
