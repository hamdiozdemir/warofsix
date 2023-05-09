from django.urls import path
from . import views

app_name = "alliances"

urlpatterns = [
    path('', views.AllianceListView.as_view(), name="alliances"),
    path('create/', views.AllianceCreateView.as_view(), name="alliance_create"),
    path('update/', views.AllianceUpdateView.as_view(), name="alliance_update"),
    path('<int:pk>/', views.AllianceDetailView.as_view(), name='alliance_detail'),
    path('my_ally/', views.MyAllyView.as_view(), name="my_ally"),
    path('new-campaign/', views.NewAllyCampaign.as_view(), name="new-campaign"),
    path('campaign/<int:pk>/', views.AllyCampaignDetailView.as_view(), name="campaign_detail"),
    path('cancel-campaign-troop/<int:campaign_id>/<int:position>/', views.cancel_campaign_troop_view, name="cancel_campaign_troop"),
    path('kick/<int:alliance_id>/<int:member_id>/', views.kick_user, name="kick_user"),
    
]
