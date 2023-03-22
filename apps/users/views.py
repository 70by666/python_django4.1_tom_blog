from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.views import PasswordChangeView

from apps.users.forms import LoginForm, RegisterForm, UserUpdateForm, ChangePasswordForm
from apps.users.models import User
from common.mixins import ProfileTitleMixin, TitleMixin, ObjectSuccessProfileMixin


class ProfileView(ProfileTitleMixin, LoginRequiredMixin, DetailView):
    """
    Контроллер профиля
    """
    template_name = 'users/profile.html'
    model = User


class ProfileEditView(ObjectSuccessProfileMixin, SuccessMessageMixin, 
                      ProfileTitleMixin, LoginRequiredMixin, UpdateView):
    """
    Контроллер редактирования прфоиля
    """
    template_name = 'users/profile_edit.html'    
    form_class = UserUpdateForm
    model = User
    success_message = 'Профиль изменен!'


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

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy(
                'users:profile', 
                args=(self.request.user.slug,)
            ))
            
        return super().dispatch(request, *args, **kwargs)


class ChangePasswordView(ObjectSuccessProfileMixin, ProfileTitleMixin, 
                         SuccessMessageMixin, PasswordChangeView):
    """
    Контроллер для изменения пароля
    """
    template_name = 'users/changepassword.html'
    title = 'Изменение пароля'
    form_class = ChangePasswordForm
