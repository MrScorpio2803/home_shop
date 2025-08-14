from django.shortcuts import render, redirect
from django.views import View

from users.forms import UserLoginForm, UserRegisterForm, UserEditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


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
                if req.POST.get('next', None):
                    return redirect(req.POST.get('next'))
                return redirect('main:index')
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль')

        return render(req, 'users/login.html', context={'form': form})


class RegisterView(View):
    def get(self, req):
        form = UserRegisterForm()
        context = {'form': form}
        return render(req, 'users/registration.html', context=context)

    def post(self, req):
        form = UserRegisterForm(data=req.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            login(req, user)
            return redirect('main:index')

        return render(req, 'users/registration.html', context={'form': form})


class ProfileView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def get(self, req):
        form = UserEditForm(instance=req.user)
        context = {'form': form}
        return render(req, 'users/profile.html', context=context)

    def post(self, req):
        form = UserEditForm(data=req.POST, instance=req.user, files=req.FILES)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
        return render(req, 'users/profile.html', context={'form': form})


class LogoutView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def get(self, req):
        return self.post(req)

    def post(self, req):
        logout(req)
        return redirect('main:index')


class CartView(View):
    def get(self, req):
        return render(req, 'cart/cart.html')
