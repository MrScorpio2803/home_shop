from django.shortcuts import render, reverse
from django.views import View

from users.forms import UserLoginForm
from django.contrib.auth import authenticate, login


class LoginView(View):

    def get(self, req):
        form = UserLoginForm()
        context = {'form': form}
        return render(req, 'users/login.html', context=context)

    def post(self, req):
        form = UserLoginForm(data=req.POST)
        if form.is_valid():
            username = req.POST['username']
            password = req.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(req, user)
                return reverse('main:index')


class RegisterView(View):
    def get(self, req):
        context = {}
        return render(req, 'users/registration.html', context=context)


class ProfileView(View):
    def get(self, req):
        context = {}
        return render(req, 'users/profile.html', context=context)


class LogoutView(View):
    pass

# Create your views here.
