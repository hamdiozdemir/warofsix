from django.urls import path
from . import views

urlpatterns = [
    path('', views.AccountsHomeView.as_view(), name="accounts"),
    path('register', views.register, name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.logout_view, name="logout"),

]