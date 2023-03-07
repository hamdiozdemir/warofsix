from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm
from django.contrib.auth import logout
from django.views.generic import TemplateView
# Create your views here.

class AccountsHomeView(TemplateView):
    template_name = "accounts/accounts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_id'] = user.id
        return context


class UserLoginView(LoginView):
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session["user_id"] = self.request.user.id
        return response


def logout_view(request):
    logout(request)
    return redirect('accounts')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            return redirect('accounts')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})