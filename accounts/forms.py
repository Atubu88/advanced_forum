from django import forms
from .models import Comment
from .models import Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': 'Комментарий',  # Измените "Комментарий" на нужный вам текст
        }

