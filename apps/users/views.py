from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from apps.users.models import User
from apps.users.forms import UserUpdateForm
from common.mixins import ProfileMixin


class ProfileView(ProfileMixin, LoginRequiredMixin, DetailView):
    template_name = 'users/profile.html'
    model = User


class ProfileEditView(ProfileMixin, LoginRequiredMixin, UpdateView):
    template_name = 'users/profile_edit.html'    
    form_class = UserUpdateForm
    model = User

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.slug,))
    
    def get_queryset(self):
        queryset = User.objects.get(slug=self.kwargs['slug'])
        
        return queryset
