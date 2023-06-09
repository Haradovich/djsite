from django import template
from women.models import *

register = template.Library()

@register.simple_tag(name='getcats')
def get_categories(filter = None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk = filter)
    
@register.simple_tag(name='getmenu')
def get_menu():
    menu = [{'title' : 'О сайте', 'url_name' : 'about'},
    {'title' : "Добавить статью", 'url_name' : 'addpost'},
    {'title' : "Обратная связь", 'url_name' : 'contact'}]
    return menu


@register.inclusion_tag('women/list_categories.html')
def show_categories(sort = None, cat_selected = 0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {'cats' : cats, 'cat_selected': cat_selected}

