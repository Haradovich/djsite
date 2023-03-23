from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from women.models import *
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

# class AddPostForm(forms.Form):  #создание формы не связанной с моделью
#     title = forms.CharField(max_length=255, label='Заголовок')
#     slug = forms.SlugField(max_length=255, label = 'URL')
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols' : 60, 'rows' : 8}), label='Текст статьи')
#     is_published = forms.BooleanField(label='Опубликовать', required=False, initial=True)
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), label= 'Выбрать категорию', empty_label='Категория не выбрана')

class AddPostForm(forms.ModelForm): #Создание формы связанной с моделью
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label= 'Выбрать категорию', empty_label='Категория не выбрана')
    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs = {'cols':80, 'rows':12})
        }

    def clean_title(self):  
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина заголовка превышает 200 символов')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class':'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols':90, 'rows':15}))
    captcha = CaptchaField()




       
