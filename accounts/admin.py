from django.contrib import admin
from .models import Category, Subcategory, Topic, Comment, Notification, Subscription

# Простая регистрация моделей без дополнительной настройки
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Subscription)
