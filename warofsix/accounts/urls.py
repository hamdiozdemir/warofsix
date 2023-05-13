from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts_redirect_view, name="accounts"),
    # path('register', views.register, name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.logout_view, name="logout"),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile'),
    path('profile/edit', views.ProfileEditView.as_view(), name="profile_edit"),
    path('profiles', views.ProfileListView.as_view(), name="profile_list"),

]