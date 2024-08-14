from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='subcategories', db_index=True)  # Добавление индекса
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Topic(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='topics', db_index=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='topics', db_index=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['subcategory', 'author']),
        ]

class Comment(models.Model):
    topic = models.ForeignKey(Topic, related_name='comments', on_delete=models.CASCADE, db_index=True)
    body = models.TextField()
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.topic}'

    class Meta:
        permissions = [
            ("can_delete_any_comment", "Can delete any comment"),
        ]

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)  # Добавление индекса
    message = models.TextField()  # Текст уведомления
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания уведомления
    is_read = models.BooleanField(default=False, db_index=True)
    related_topic = models.ForeignKey('Topic', on_delete=models.CASCADE, null=True, blank=True)  # Связь с темой# Статус прочтения уведомления

    def __str__(self):
        return f"Notification for {self.user.username}"

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, подписанный на тему
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # Тема, на которую подписан пользователь
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания подписки

    def __str__(self):
        return f"{self.user.username} subscribed to {self.topic.title}"
