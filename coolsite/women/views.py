from typing import Any, Dict
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect,  get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout, login
from .models import *
from .forms import *
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin




# def index(request):
#     posts = Women.objects.all()
#     data = {
#         'title': 'Главная страница',
#         'posts' : posts,
#         'cat_selected' : 0,

#     }
#     return render(request, 'women/index.html', context = data)

class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    paginate_by = 15

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Главная страница')
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_queryset(self):
        return Women.objects.filter(is_published = True).select_related('cat')


def about(request):
    return render(request, 'women/about.html', {'title' : 'О сайте'})

class AddPost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpost.html'
    success_url = reverse_lazy('home')
    login_url = '/admin/'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Добавление записи')
        return dict(list(context.items()) + list(c_def.items()))



# def addpost(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')            
#     else:
#         form = AddPostForm()

#     data = {
#         'title' : 'Добавление записи',
#         'form' : form,

#     }
#     return render(request, 'women/addpost.html', context = data)


# def contact(request):
#     pass

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form) -> HttpResponse:
        print(form.cleaned_data)
        return redirect('home')




class WomenPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        post = Women.objects.get(slug = self.kwargs['post_slug'])
        c_def = self.get_user_context(title = post.title, cat_selected = post.cat_id)
        return dict(list(context.items()) + list(c_def.items()))

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug = post_slug)
#     data = {
#         'title' : post.title,
#         'post' : post,
#         'cat_selected' : post.cat_id,
#     }
#     return render(request, 'women/post.html', context = data)

class WomenCategory(DataMixin, ListView):
    paginate_by = 2
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cat = Category.objects.get(slug = self.kwargs['cat_slug'])
        c_def = self.get_user_context(title = cat.name, cat_selected = cat.pk)
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_queryset(self):
        return Women.objects.filter(cat__slug = self.kwargs['cat_slug'], is_published = True).select_related('cat')
    
# def show_category(request, cat_slug):
#     category_name = Category.objects.get(slug = cat_slug)
#     posts = Women.objects.filter(cat_id = category_name.pk)
#     if len(posts) == 0:
#         raise Http404
#     data = {
#         'title': category_name,
#         'posts' : posts,
#         'cat_selected' : category_name.pk,

#     }
#     return render(request, 'women/index.html', context = data)

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Регистрация')
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
    

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Аутентификация')
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_success_url(self) -> str:
        return reverse_lazy('home')
    

def logout_user(request):
    logout(request)
    return redirect('home')



def category(request, catid):
    if(request.GET):
        print(request.GET)
    return HttpResponse(f'<h1>Статьи по категории № {catid}</h1>')

def archive(request, year):
    if int(year) > 2024:
        return redirect('home', permanent=True)
    return HttpResponse(f'<h1> Год: {year} </h1>')

def pagenotfound(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена </h1>')