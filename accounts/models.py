from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Topic(models.Model):
    subcategory = models.ForeignKey(Subcategory, related_name='topics', on_delete=models.CASCADE)
    content = models.TextField()
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    topic = models.ForeignKey(Topic, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.topic}'

    class Meta:
        permissions = [
            ("can_delete_any_comment", "Can delete any comment"),
        ]


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, которому предназначено уведомление
    message = models.TextField()  # Текст уведомления
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания уведомления
    is_read = models.BooleanField(default=False)  # Статус прочтения уведомления

    def __str__(self):
        return f"Notification for {self.user.username}"

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, подписанный на тему
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # Тема, на которую подписан пользователь
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания подписки

    def __str__(self):
        return f"{self.user.username} subscribed to {self.topic.title}"
