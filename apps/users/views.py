from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from apps.users.models import User, Profile
from apps.users.forms import ProfileUpdateForm, UserUpdateForm
from common.mixins import ProfileMixin


class ProfileView(ProfileMixin, LoginRequiredMixin, DetailView):
    template_name = 'users/profile.html'
    model = Profile


class ProfileEditView(ProfileMixin, LoginRequiredMixin, UpdateView):
    template_name = 'users/profile_edit.html'    
    form_class = ProfileUpdateForm
    model = Profile

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.profile.slug,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_update_from'] = UserUpdateForm(
                self.request.POST, 
                instance=self.request.user
            )
        else:
            context['user_update_from'] = UserUpdateForm(instance=self.request.user)
        
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form = context['user_update_from']
        if form.is_valid():
            form.save()
        else:
            context['error'] = 'Что-то не так, проверьте введенные данные и повторите попытку.'
            return self.render_to_response(context)

        return super().form_valid(form)
