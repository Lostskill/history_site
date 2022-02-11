from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from .utils import * 
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout , login


class HeroesHome(DataMixin, ListView): 
    
    model = Heroes
    template_name = 'heroes/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная Страница') 
        
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Heroes.objects.filter(is_published=True).select_related('rub')


# def index(request):
#     posts = Women.objects.all()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'women/index.html', context=context)

def about(request):
    return render(request, 'heroes/about.html', {'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'heroes/addpage.html'
    success_url = reverse_lazy('home') 
    login_url = reverse_lazy('home') 
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи') 
        return dict(list(context.items()) + list(c_def.items()))


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})

class ContactFormView(DataMixin, FormView):
    form_class = ContacForm 
    template_name = 'heroes/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self,form):
        print(form.cleaned_data)
        return redirect('home')

#def login(request):
#    return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'women/post.html', context=context)

class ShowPost(DataMixin, DetailView):
    model = Heroes
    template_name = 'heroes/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи') 
        return dict(list(context.items()) + list(c_def.items()))

 


class HeroesCategory(DataMixin, ListView):
     
    model = Heroes
    template_name = 'heroes/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Heroes.objects.filter(rub__slug=self.kwargs['rub_slug'], is_published=True).select_related('rub')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug = self.kwargs['rub_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),rub_selected=c.pk) 
        return dict(list(context.items()) + list(c_def.items()))


# def show_category(request, cat_id):
#     posts = Women.objects.filter(cat_id=cat_id)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_id,
#     }
#
#     return render(request, 'women/index.html', context=context)

class RegisterUser(DataMixin, CreateView):

    form_class = RegisterUserForm
    template_name = 'heroes/register.html'
    success_url = reverse_lazy('login') 

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация Пользователя') 
        return dict(list(context.items()) + list(c_def.items())) 

    def form_valid(self,form):
        user = form.save()
        login(self.request,user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm 
    template_name = 'heroes/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация') 
        return dict(list(context.items()) + list(c_def.items()))     

    def get_success_url(self):
        return reverse_lazy('home') 

def logout_user(request):
    logout(request)
    return redirect('login')
