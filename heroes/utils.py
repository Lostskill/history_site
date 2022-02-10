
from .models import *
from django.db.models import Count

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
]

class DataMixin:
    paginate_by = 4

    def get_user_context(self, **kwargs):
        context = kwargs
        rubs = Category.objects.annotate(Count('heroes'))
        
        
        user_menu = menu.copy()
        if not self.request.user.is_authenticated :
            user_menu.pop(1)
        
        context['menu'] = user_menu
        context['rubs'] = rubs
        if 'rub_selected' not in context:
            context['rub_selected'] = 0
        return context