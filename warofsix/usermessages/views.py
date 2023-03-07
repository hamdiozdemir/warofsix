from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from main.models import Messages, UserTracker
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from .forms import MessageCreateForm
# Create your views here.

class UserTestMixin(LoginRequiredMixin, UserPassesTestMixin):
    permission_denied_message = "You are not authorized to view this page."
    raise_exception = False

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def handle_no_permission(self):
        # Redirect the user to a different page
        return redirect('settlement')



class MessageInboxView(LoginRequiredMixin, ListView):
    model = Messages
    template_name = "usermessages/inbox.html"
    context_object_name = "inbox"

    def get_queryset(self):
        return Messages.objects.filter(target = self.request.user).order_by('-time')


class MessageSentView(LoginRequiredMixin, ListView):
    model = Messages
    template_name = "usermessages/sent.html"
    context_object_name = "sent"

    def get_queryset(self):
        return Messages.objects.filter(sender = self.request.user).order_by('-time')
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user=self.request.user
        tracker= UserTracker.objects.get(user=user)
        tracker.track += 1
        tracker.save()
        return context



class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Messages
    template_name = "usermessages/message_detail.html"
    context_object_name = "message"

    def get_queryset(self):
        return Messages.objects.filter(Q(sender=self.request.user) | Q(target=self.request.user))
    
    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs["pk"])
        if obj:
            obj.is_read = True
            obj.save()
        return obj
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user=self.request.user
        tracker= UserTracker.objects.get(user=user)
        tracker.track += 1
        tracker.save()
        return context

    

class MessageCreateView(CreateView):
    model = Messages
    form_class = MessageCreateForm
    template_name = "usermessages/new_message.html"
    # success_url = reverse_lazy('usermessages:inbox')

    def form_valid(self, form):
        message = form.save(commit=False)
        message.sender = self.request.user
        message.save()
        return redirect('/usermessages/inbox')


@login_required
def messages_view(request):
    user = request.user
    tracker = UserTracker.objects.get(user=user)
    tracker.track += 1
    tracker.save()

    inbox = Messages.objects.filter(target=user)
    context = {"inbox": inbox}
    return render(request, "main/messages.html", context)


@login_required
def messages_sent_view(request):
    user = request.user
    tracker = UserTracker.objects.get(user=user)
    tracker.track += 1
    tracker.save()

    sent = Messages.objects.filter(sender=user)
    context = {"sent": sent}
    return render(request, "main/messages_sent.html", context)