from django.test import TestCase
from django.contrib.auth.models import User
from .models import Topic, Comment, Subscription, Notification, Category, Subcategory


class NotificationTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.category = Category.objects.create(name='Test Category')  # Создаем категорию
        self.subcategory = Subcategory.objects.create(name='Test Subcategory',
                                                      category=self.category)  # Создаем подкатегорию с категорией
        self.topic = Topic.objects.create(title='Test Topic', body='Test Body', author=self.user1,
                                          subcategory=self.subcategory)
        Subscription.objects.create(user=self.user1, topic=self.topic)
        Subscription.objects.create(user=self.user2, topic=self.topic)

    def test_notification_created_for_subscribers(self):
        self.client.login(username='user1', password='password1')
        response = self.client.post(f'/topic/{self.topic.id}/', {'body': 'Test Comment'})
        self.assertEqual(response.status_code, 302)

        notifications_user1 = Notification.objects.filter(user=self.user1)
        notifications_user2 = Notification.objects.filter(user=self.user2)

        self.assertEqual(notifications_user1.count(), 0)
        self.assertEqual(notifications_user2.count(), 1)
        self.assertIn('New comment on Test Topic', notifications_user2[0].message)

    def test_notification_not_created_for_author(self):
        self.client.login(username='user2', password='password2')
        response = self.client.post(f'/topic/{self.topic.id}/', {'body': 'Another Test Comment'})
        self.assertEqual(response.status_code, 302)

        notifications_user1 = Notification.objects.filter(user=self.user1)
        notifications_user2 = Notification.objects.filter(user=self.user2)

        self.assertEqual(notifications_user2.count(), 0)
        self.assertEqual(notifications_user1.count(), 1)
        self.assertIn('New comment on Test Topic', notifications_user1[0].message)
