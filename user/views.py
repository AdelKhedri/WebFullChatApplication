from django.shortcuts import render, redirect
from django.views import View
from .models import User, Profile
from .forms import UserLoginForm, UserCreateForm, UserChangeForm, ProfileChangeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin


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
        return render(request, self.template_name, {'form': userForm})
    

class ChangeProfileView(LoginRequiredMixin, View):
    template_name = 'user/edite_profile.html'
    login_url = '/login/'

    # def setup(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         self.
    #     super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        context = {
            'profile_form': ProfileChangeForm(instance=request.user.profile),
            'user_form': UserChangeForm(instance=request.user),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        profile_form = ProfileChangeForm(request.FILES, request.POST, instance=request.user.profile)
        user_form = UserChangeForm(request.POST, instance=request.user)

        if profile_form.is_valid():
            profile_form.save()
        if user_form.is_valid():
            user_form.save()
        
        context = {
            'profile_form': profile_form,
            'user_form': user_form,
        }
        return render(request, self.template_name, context)