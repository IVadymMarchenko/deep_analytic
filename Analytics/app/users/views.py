# Create your views here.
from django.shortcuts import render,redirect
from .forms import UserLoginForm,UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.urls import reverse,reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login as auth_login
# Create your views here.


class BaseView(TemplateView):
    template_name = 'users/registr_form.html'


class UserLoginView(LoginView):
    template_name = 'users/registr_form.html'  # Указ cшаблон для логина
    form_class = UserLoginForm  # Указ свою форму


    def form_valid(self, form):
        """Called if the form is valid.."""
        user = form.get_user()
        auth.login(self.request, user)
        return super().form_valid(form)
        

    def form_invalid(self, form):
        """ Method that is called when form validation fails """
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)  # Отоб ошибки формы
    
    def get_success_url(self):
        """
         It Returns the url to redirect after successful login.
        """
        user = self.request.user
        if user.is_authenticated:
            return reverse('profile:profile', kwargs={'username': user.username, 'user_id': user.id})
        return reverse('users:login')



def registration(request):
    if request.method == "POST":
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем форму и получаем объект пользователя
            auth.login(request, user)  # Выполняем вход в систему
            # Редирект на профиль пользователя с передачей username и user_id
            return redirect(reverse('profile:profile', kwargs={'username': user.username, 'user_id': user.id}))
    else:
        form = UserRegisterForm()
    context = {
        "title": "Registration",
        "form": form
    }
    return render(request, 'users/registr_form.html', context)

@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('users:users'))