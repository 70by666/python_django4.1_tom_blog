from django import forms

from apps.blog.models import Posts
from common.mixins import InitFormMixin


class NewPostForm(InitFormMixin, forms.ModelForm):
    """
    Форма для добавления постов
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {"placeholder": 'Придумайте название статьи'}
        )
        self.fields["short_description"].widget.attrs.update(
            {"placeholder": 'Напишите короткое описание статьи'}
        )
        self.fields["full_description"].widget.attrs.update(
            {"placeholder": 'Напишите полное описание статьи'}
        )
        
    class Meta:
        model = Posts
        fields = (
            'category', 'image', 'title', 
            'short_description', 'full_description', 'status'
        )
