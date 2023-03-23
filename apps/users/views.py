from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages

from apps.users.forms import LoginForm, RegisterForm, UserUpdateForm, ChangePasswordForm
from apps.users.models import User
from apps.users.tasks import send_email_verify
from common.mixins import ProfileTitleMixin, TitleMixin, ObjectSuccessProfileMixin


import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from apps.users.models import EmailVerification, User


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
    
    def form_valid(self, form):
        new_email = self.object.email
        old_email = self.model.objects.get(id=self.request.user.id).email
        if new_email != old_email:
            messages.info(
                self.request,
                'На ваш адрес электронной почты было отправлено письмо с '
                'подтверждением. Пожалуйста, проверьте свою почту '
                'и перейдите по ссылке, иначе вы не сможете авторизоваться. '
                'Если письмо не пришло, проверьте папку спам.'
            )
            send_email_verify.delay(self.request.user.id, new_email)
        
        super().form_valid(form)
        
        return redirect('users:login')


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


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_confirmed.html'
    title = 'Электронная почта подтверждена'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        emailverifications = EmailVerification.objects.filter(user=user,
                                                              code=code)
        if emailverifications.exists() and emailverifications.first().is_expired():
            user.is_active = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return redirect('users:email_failed')


class EmailVerificationFailedView(TitleMixin, TemplateView):
    template_name = 'users/email_failed.html'
    title = 'Электронная почта не подтверждена'
