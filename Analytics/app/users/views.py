# Create your views here.
from django.shortcuts import render,redirect
from .forms import UserLoginForm,UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.urls import reverse,reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView,CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseRedirect
from .utils import BaseAuthView
# Create your views here.


class BaseView(TemplateView):
    template_name = 'users/registr_form.html'


class UserRegistrationView(BaseAuthView, CreateView):
    template_name = 'users/registr_form.html'
    form_class = UserRegisterForm

    def form_valid(self, form):
        """Handle successful registration."""
        user = form.save()  # Save the form and get the user instance
        auth.login(self.request, user)  # Log the user in
        return HttpResponseRedirect(self._get_profile_url(user))


class UserLoginView(BaseAuthView, LoginView):
    template_name = 'users/registr_form.html'
    form_class = UserLoginForm

    def form_valid(self, form):
        """Handle successful login."""
        user = form.get_user()
        auth.login(self.request, user)  # Log the user in
        return HttpResponseRedirect(self._get_profile_url(user))

    def form_invalid(self, form):
        """Handle invalid form submission."""
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)



@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('users:users'))