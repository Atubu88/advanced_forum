from .models import Notification, Subscription
from django.urls import reverse

def send_notification(user, message):
    Notification.objects.create(user=user, message=message)


def notify_subscribers(comment):
    topic = comment.topic
    subscribers = Subscription.objects.filter(topic=topic)
    for subscription in subscribers:
        if subscription.user != comment.author:
            comment_url = f'{reverse("topic_detail", args=[topic.id])}#comment-{comment.id}'
            notification_message = f'<a href="{comment_url}">Новое сообщение в теме: {topic.title}</a>'
            Notification.objects.create(user=subscription.user, message=notification_message)

