import pytest
from django.core.cache import cache
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from views import forum_home
from models import Category, Notification

@pytest.mark.django_db
def test_forum_home_with_cached_categories():
    factory = RequestFactory()
    request = factory.get(reverse('forum_home'))
    request.user = AnonymousUser()

    # Создаем категории и сохраняем их в кэш
    categories = [Category.objects.create(name='Category 1'), Category.objects.create(name='Category 2')]
    cache.set('categories', categories)

    response = forum_home(request)
    assert response.status_code == 200
    assert 'categories' in response.context_data
    assert response.context_data['categories'] == categories

@pytest.mark.django_db
def test_forum_home_without_cached_categories():
    factory = RequestFactory()
    request = factory.get(reverse('forum_home'))
    request.user = AnonymousUser()

    # Убедимся, что кэш пуст
    cache.clear()

    # Создаем категории в базе данных
    categories = [Category.objects.create(name='Category 1'), Category.objects.create(name='Category 2')]

    response = forum_home(request)
    assert response.status_code == 200
    assert 'categories' in response.context_data
    assert list(response.context_data['categories']) == categories

@pytest.mark.django_db
def test_forum_home_authenticated_user():
    factory = RequestFactory()
    user = User.objects.create_user(username='testuser', password='12345')
    request = factory.get(reverse('forum_home'))
    request.user = user

    # Создаем уведомления для пользователя
    notifications = [Notification.objects.create(user=user, is_read=False)]

    response = forum_home(request)
    assert response.status_code == 200
    assert 'notifications' in response.context_data
    assert list(response.context_data['notifications']) == notifications
