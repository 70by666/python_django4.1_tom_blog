class TitleMixin:
    """
    Миксин для заголовка страницы в представлениях
    """
    title = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        
        return context


class ProfileMixin:
    """
    Миксин для заголовка страницы в представлениях профиля и его редактирования
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.id} - {self.object.username}'
        
        return context


class InitFormMixin:
    """
    Миксин для применения стилей к input в формах
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off',
            })
