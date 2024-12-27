# Create your views here.
from django.shortcuts import render,redirect
from .forms import UserLoginForm,UserRegisterForm
from django.contrib import auth
from django.urls import reverse
from django.contrib import messages

# Create your views here.


def base(request):
    return render(request,'users/registr_form.html')


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)  # Передаем данные из POST в форму
        if form.is_valid():
            email = form.cleaned_data['email']  # Получаем очищенные данные
            password = form.cleaned_data['password']
            user= auth.authenticate(request, email=email,password=password)
            if user:
                auth.login(request,user)
                return redirect(reverse('profile:prifile'))
        else:
            messages.error(request, form.non_field_errors())  # Добавляем сообщение об ошибке       
    else:
        form = UserLoginForm() 
    context = {
        'title': 'Auth',
        'form': form
    }
    return render(request, 'users/registr_form.html', context)


def registration(request):
    if request.method=="POST":
        form= UserRegisterForm(data=request.POST)
        print('Form errors:', form.errors)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request,user)
            return redirect(reverse('app_profile:profile'))
    else:
        form=UserRegisterForm()
        print('Form errors:', form.errors)
    context = {"title":"Registration",
               "form": form}
    return render(request, 'users/registr_form.html', context)






def logout(request):
    pass