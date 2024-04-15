from django.shortcuts import render, redirect
from django.views import View
from .models import User, Profile
from .forms import UserLoginForm, UserCreateForm
from django.contrib.auth import authenticate, login


class LoginView(View):
    template_name = 'user/login.html'

    def get(self, request, *args, **kwargs):
        userForm = UserLoginForm()
        return render(request, self.template_name, {'form': userForm})
    
    def post(self, request, *args, **kwargs):
        userForm = UserLoginForm(request.POST)
        
        if userForm.is_valid():
            phone_number = userForm.cleaned_data['phone_number']
            password = userForm.cleaned_data['password']
            user = authenticate(request, phone_number=phone_number, password=password)
            print(user)
            if user is not None:
                login(request, user=user)
                return redirect('/admin/')
        
        return render(request, self.template_name, {'form': userForm})


class SinUpView(View):
    template_name = 'user/sinup.html'
    
    def get(self, request, *args, **kwargs):
        userForm = UserCreateForm()
        return render(request, self.template_name, {'form': userForm})
    
    def post(self, request, *args, **kwargs):
        userForm = UserCreateForm(request.POST)
        if userForm.is_valid():
            userForm.save()
            userForm = UserCreateForm()
        return render(request, self.template_name, {'form': userForm})