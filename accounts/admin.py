from django.contrib import admin
from .models import Category, Subcategory, Topic, Comment

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Topic)
admin.site.register(Comment)
