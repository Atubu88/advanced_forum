from django.urls import path
from .views import forum_home, SubcategoryTopicsView, TopicDetailView
from .views import edit_comment, delete_comment

urlpatterns = [
    path('', forum_home, name='forum_home'),
    path('subcategory/<int:subcategory_id>/', SubcategoryTopicsView.as_view(), name='subcategory_topics'),
    path('topic/<int:topic_id>/', TopicDetailView.as_view(), name='topic_detail'),
    path('comment/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
]
