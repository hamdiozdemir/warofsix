from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.HomeView.as_view(), name="index"),
    path('resources', views.ResourcesDetailView.as_view(), name="resources"),
    path('settlement', views.SettlementView.as_view(), name="settlement"),
    path('building/<int:settlement_id>/', views.building_view, name="building"),
    path('building_update/<int:settlement_id>/<int:builder>/', views.building_update, name="building_update"),
    path('building/<int:settlement_id>/<str:action>/', views.building_update_cancel, name="building_update_cancel"),
    path('new_building/<int:settlement_id>/', views.new_building, name="new_building"),
    path('armory/<int:settlement_id>/', views.armory_view, name="armory"),
    path('fortress/<int:settlement_id>/', views.fortress_view, name="fortress"),
    path('market/<int:settlement_id>/', views.market_view, name="market_view"),
    path('market/<int:settlement_id>/accept/<int:exchange_id>/', views.market_accept_offer, name="market_accept_offer"),
    path('market/<int:settlement_id>/cancel/<int:exchange_id>/', views.market_cancel_offer, name="market_cancel_offer"),
    path('user/<int:user_id>/', views.profile_redirect_view, name="profile_redirect_view"),
    path('fortress/power_report/<int:pk>/', views.SuperPowerReportsView.as_view(), name="power_reports"),
    path('no-auth', views.no_auth_view, name="no_auth"),
    path('guide/', views.GuideView.as_view(), name="guide"),




]
