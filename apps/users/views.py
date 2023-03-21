from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from apps.users.forms import LoginForm, RegisterForm, UserUpdateForm
from apps.users.models import User
from common.mixins import ProfileTitleMixin, TitleMixin


class ProfileView(ProfileTitleMixin, LoginRequiredMixin, DetailView):
    """
    Контроллер профиля
    """
    template_name = 'users/profile.html'
    model = User


class ProfileEditView(SuccessMessageMixin, ProfileTitleMixin, LoginRequiredMixin, UpdateView):
    """
    Контроллер редактирования прфоиля
    """
    template_name = 'users/profile_edit.html'    
    form_class = UserUpdateForm
    model = User
    success_message = 'Профиль изменен!'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.slug,))


class LoginView(TitleMixin, LoginView):
    """
    Контроллер авторизации
    """
    template_name = 'users/login.html'
    title = 'Авторизация'
    form_class = LoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.slug,))


class RegisterView(TitleMixin, SuccessMessageMixin, CreateView):
    """
    Контроллер регистрации
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
