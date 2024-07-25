from django import forms
from .models import Comment
from .models import Topic
from allauth.account.forms import LoginForm, SignupForm
from django.utils.translation import gettext_lazy as _


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']
        labels = {
            'title': 'Название темы',
            'content': 'Содержание',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': 'Комментарий',  # Измените "Комментарий" на нужный вам текст
        }

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'class': 'form-control', 'id': 'login', 'name': 'login'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'id': 'password', 'name': 'password'})
# accounts/forms.py



class CustomSignupForm(SignupForm):
    email = forms.EmailField(required=False, label=_('Электронная почта'))

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': _('Имя пользователя'),
            'email': _('Электронная почта'),
            'password1': _('Пароль'),
            'password2': _('Подтвердите пароль'),
        }

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            if fieldname in self.fields:
                self.fields[fieldname].help_text = None

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data