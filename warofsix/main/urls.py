from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.HomeView.as_view(), name="index"),
    path('resources', views.ResourcesDetailView.as_view(), name="resources"),
    path('settlement', views.SettlementView.as_view(), name="settlement"),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile'),
    path('building/<int:settlement_id>/', views.building_view, name="building"),
    path('building_update/<int:settlement_id>/<int:builder>/', views.building_update, name="building_update"),
    path('resource/<str:resource_type>/', views.resource_builder_update_view, name="resource_update"),
    path('building/<int:settlement_id>/<str:action>/', views.building_update_cancel, name="building_update_cancel"),
    path('new_building/<int:settlement_id>/', views.new_building, name="new_building"),
    path('armory/<int:settlement_id>/', views.armory_view, name="armory"),
    path('fortress/<int:settlement_id>/', views.fortress_view, name="fortress"),



]
