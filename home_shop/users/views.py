from django.db.models.base import Model as Model
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView, TemplateView

from cart.models import Cart
from users.forms import UserLoginForm, UserRegisterForm, UserEditForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class UserLoginView(LoginView):

    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('main:index')

    def get_success_url(self) -> str:
        page = self.request.POST.get('next', None)
        if page and page != reverse_lazy('users:login'):
            return page
        return reverse_lazy('main:index')
    
    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()
        if user:
            login(self.request, user)
            old_carts = Cart.objects.filter(user=user)
            if old_carts.exists():
                for cart in old_carts:
                    product = cart.product
                    check_product = Cart.objects.filter(product=product, session_key=session_key).first()
                    if check_product:
                        check_product.quantity += cart.quantity
                        check_product.save()
                        cart.delete()
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
            return super().form_valid(form)


class RegisterView(CreateView):
    
    template_name = 'users/registration.html'
    form_class = UserRegisterForm
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            login(self.request, user)
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
        
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('main:index')



class ProfileView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('users:login')
    template_name = 'users/profile.html'
    form_class = UserEditForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset = None) -> Model:
        return self.request.user
    


# class LogoutView(LoginRequiredMixin, LogoutView):
#     login_url = reverse_lazy('users:login')
#     def get_s


class CartView(TemplateView):
    template_name = 'cart/cart.html'

