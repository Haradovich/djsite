from django.contrib import admin
from django.urls import path, include, re_path
from women.views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', WomenHome.as_view(), name='home'),
    path('about/', about, name = 'about'),
    path('addpost/', AddPost.as_view(), name = 'addpost'),
    path('contact/', ContactFormView.as_view(), name = 'contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', WomenPost.as_view(), name = 'post'),
    path('category/<slug:cat_slug>', WomenCategory.as_view(), name = 'show_category'),

    re_path(r'^archive/(?P<year>[0-9]{4})/', archive, name='archive')
]