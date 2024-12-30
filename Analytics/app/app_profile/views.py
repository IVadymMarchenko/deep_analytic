from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def get_profile(request,username,user_id):
    return render(request,'app_profile/profile.html')