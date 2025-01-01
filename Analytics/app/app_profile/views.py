from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import CustomUser


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'app_profile/profile.html'
    redirect_url = 'profile:profile'

    def dispatch(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        if int(user_id) != self.request.user.id:
            # Redirect to your profile page if the ID does not match
            return redirect(reverse(self.redirect_url, kwargs={'username': self.request.user.username, 'user_id': self.request.user.id}))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        context['username'] = self.kwargs.get('username')
        context['user_id'] = user_id
        context['user'] = get_object_or_404(CustomUser, id=user_id)
        return context