from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, TemplateView,
                                  UpdateView, ListView)
from django.core.cache import cache

from apps.blog.models import Posts
from apps.users.forms import (ChangePasswordForm, LoginForm, RegisterForm,
                              UserUpdateForm)
from apps.users.models import EmailVerification, User
from apps.users.tasks import send_email_verify
from common.mixins import (ObjectSuccessProfileMixin, ProfileTitleMixin,
                           TitleMixin)

message_email = 'На ваш адрес электронной почты было отправлено письмо с '\
                'подтверждением. Пожалуйста, проверьте свою почту '\
                'и перейдите по ссылке, иначе вы не сможете авторизоваться. '\
                'Если письмо не пришло, проверьте папку спам или обратитесь к '\
                'к администрации.'
                

class ProfileView(ProfileTitleMixin, LoginRequiredMixin, DetailView):
    """
    Контроллер профиля
    """
    template_name = 'users/profile.html'
    model = User
    
    def get_context_data(self, **kwargs):
        """
        Вывод последних 6 постов определенного автора
        """
        context = super().get_context_data(**kwargs)
        context["last_posts"] = (
            Posts.objects.select_related('author', 'category')
            .prefetch_related('likes')
            .filter(author=self.object, status=0)[:6]
        )
            
        return context
    
    
class ProfileAllPostsView(LoginRequiredMixin, ProfileTitleMixin, ListView):
    """
    Контроллер для просмотра всех постов определенного автора
    """
    model = Posts
    template_name = 'users/allposts.html'
    paginate_by = 6
    
    def get_queryset(self):
        """
        Возвращает queryset для определенного автора и кэширование
        """
        queryset = cache.get(f'queryset {self.kwargs["slug"]}')
        if not queryset:
            user = User.objects.get(slug=self.kwargs['slug'])
            queryset = super().get_queryset().filter(author=user)
            cache.set(f'queryset {self.kwargs["slug"]}', queryset, 10)
        
        return queryset


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
        """
        Отправка письма, если была изменена почта
        """
        new_email = self.object.email
        old_email = self.model.objects.get(id=self.request.user.id).email
        if new_email != old_email:
            messages.info(
                self.request,
                message_email,
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
    success_message = 'Регистрация прошла успешно!' + message_email
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        """
        Редирект авторизованного пользователя, чтобы он не мог 
        зарегистрироваться
        """
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
    """
    Контроллер для подтверждения почты
    """
    template_name = 'users/email_confirmed.html'
    title = 'Электронная почта подтверждена'

    def get(self, request, *args, **kwargs):
        """
        Проверка валидности письма
        """
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        verify = EmailVerification.objects.filter(user=user, code=code)
        if verify.exists():
            verify_obj = verify.first()
            if verify_obj.is_expired() and verify_obj.is_valid:
                user.is_active = True
                user.save()
                verify_obj.is_valid = False
                verify_obj.save()
                return super().get(request, *args, **kwargs)
            else:
                return redirect('users:email_failed')
        else:
            return redirect('users:email_failed')


class EmailVerificationFailedView(TitleMixin, TemplateView):
    """
    Контроллер для отображения неудачного подтверждения почты
    """
    template_name = 'users/email_failed.html'
    title = 'Электронная почта не подтверждена'
