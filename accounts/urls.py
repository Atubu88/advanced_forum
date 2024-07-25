from django.urls import path
from .views import forum_home, SubcategoryTopicsView, TopicDetailView, notifications_view, mark_as_read
from .views import edit_comment, delete_comment
from .views import CustomLoginView, CustomSignupView


urlpatterns = [
    path('', forum_home, name='forum_home'),
    path('subcategory/<int:subcategory_id>/', SubcategoryTopicsView.as_view(), name='subcategory_topics'),
    path('topic/<int:topic_id>/', TopicDetailView.as_view(), name='topic_detail'),
    path('notifications/', notifications_view, name='notifications'),
    path('notification/read/<int:notification_id>/', mark_as_read, name='mark_as_read'),
    path('comment/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('login/', CustomLoginView.as_view(), name='account_login'),
    path('signup/', CustomSignupView.as_view(), name='account_signup'),
]
