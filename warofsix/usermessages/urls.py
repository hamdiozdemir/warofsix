from django.urls import path
from . import views

app_name = "usermessages"

urlpatterns = [
    path('inbox', views.MessageInboxView.as_view(), name="inbox"),
    path('sent', views.MessageSentView.as_view(), name="sent"),
    path('<int:pk>/', views.MessageDetailView.as_view(), name="message_detail"),
    path('new_message', views.MessageCreateView.as_view(), name="new_message"),


]
