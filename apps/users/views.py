from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect

from apps.users.models import User
from apps.users.forms import UserUpdateForm, LoginForm, RegisterForm
from common.mixins import ProfileMixin, TitleMixin


class ProfileView(ProfileMixin, LoginRequiredMixin, DetailView):
    """
    Представление профиля
    """
    template_name = 'users/profile.html'
    model = User


class ProfileEditView(ProfileMixin, LoginRequiredMixin, UpdateView):
    """
    Представление редактирования профиля
    """
    template_name = 'users/profile_edit.html'    
    form_class = UserUpdateForm
    model = User

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.slug,))


class LoginView(TitleMixin, LoginView):
    """
    Представление авторизации
    """
    template_name = 'users/login.html'
    title = 'Авторизация'
    form_class = LoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.slug,))


class RegisterView(TitleMixin, SuccessMessageMixin, CreateView):
    """
    Представление регистрации
    """
    model = User
    template_name = 'users/register.html'
    title = 'Регистрация'
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')
    success_message = 'Регистрация прошла успешно!'
    redirect_authenticated_user = True

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy(
                'users:profile', 
                args=(self.request.user.slug,)
            ))
            
        return super().get(request, *args, **kwargs)
