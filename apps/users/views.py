from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, PasswordChangeView,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, UpdateView)

from apps.blog.models import Posts
from apps.users.forms import (ChangePasswordForm, LoginForm,
                              ProfileCommentCreateForm, RegisterForm,
                              ResetPasswordForm, SetPasswordForm,
                              UserUpdateForm)
from apps.users.models import EmailVerification, ProfileComments, User
from apps.users.tasks import send_verification_email_task
from services.mixins import (NoAuthRequiredMixin, ObjectSuccessProfileMixin,
                             ProfileTitleMixin, TitleMixin)

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
        Вывод последних 6 постов определенного автора и кэширование
        """
        context = super().get_context_data(**kwargs)
        context['form'] = ProfileCommentCreateForm
        context['comms'] = (
            ProfileComments.objects
            .select_related('user', 'author')
            .filter(user=self.object)
        )
        context["last_posts"] = cache.get(f'last_posts {self.kwargs["slug"]}')
        if not context["last_posts"]: 
            context["last_posts"] = (
                Posts.objects.select_related('author', 'category')
                .prefetch_related('likes')
                .filter(author=self.object, status=0)[:6]
            )
            cache.set(
                f'last_posts {self.kwargs["slug"]}', 
                context["last_posts"], 
                60
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
            cache.set(f'queryset {self.kwargs["slug"]}', queryset, 60)
        
        return queryset

    def get_context_data(self, **kwargs):
        """
        Передать слаг пользователя, чью посты просматриваются для корректной
        работы пагинатора
        """
        context = super().get_context_data(**kwargs)
        context["slug"] = self.kwargs['slug']
        
        return context
    

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
            send_verification_email_task.delay(self.request.user.id, new_email)
        
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


class RegisterView(NoAuthRequiredMixin, TitleMixin, SuccessMessageMixin, CreateView):
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

        return redirect('users:email_failed')


class EmailVerificationFailedView(TitleMixin, TemplateView):
    """
    Контроллер для отображения неудачного подтверждения почты
    """
    template_name = 'users/email_failed.html'
    title = 'Электронная почта не подтверждена'


class ResetPasswordView(NoAuthRequiredMixin, TitleMixin, 
                        SuccessMessageMixin, PasswordResetView):
    """
    Контроллер для отправки письма на почту, чтобы сбросить пароль
    """
    title = 'Запрос на восстновление пароля'
    form_class = ResetPasswordForm
    template_name = 'users/resetpassword.html'
    subject_template_name = 'users/email/resetemailtitle.txt'
    email_template_name = 'users/email/resetemailtext.html'
    success_message = 'Письмо для восстановления аккаунта отправлено!'
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        print(type(form.data['email']), form.data['email'])
        if not User.objects.filter(email=form.data['email']).exists():
            form.add_error('email', 'Аккаунта с такой почтой не существует!')
            return self.form_invalid(form) 
        
        return super().form_valid(form)
    

class SetPasswordView(NoAuthRequiredMixin, TitleMixin, 
                      SuccessMessageMixin, PasswordResetConfirmView):
    """
    Контроллер для установки нового пароля
    """
    title = 'Установка нового пароля'
    form_class = SetPasswordForm
    template_name = 'users/setpassword.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Установлен новый пароль, можете авторизоваться'


class FailedSetPasswordView(TitleMixin, TemplateView):
    """
    Контроллер невалидного письма сброса пароля
    """
    title = 'Ссылка недействительна'
    template_name = 'users/failedsetpassword.html'


class ProfileCommentCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    Контроллер для написания комментария под профилем
    """
    model = ProfileComments
    form_class = ProfileCommentCreateForm
    success_message = 'Комментарий добавлен'
    
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.kwargs['slug'],))

    def form_valid(self, form):
        user = User.objects.get(slug=self.kwargs['slug'])
        form.instance.user = user
        form.instance.author = self.request.user
    
        return super().form_valid(form)
