from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Category, Subcategory, Topic, Comment, Notification, Subscription
from .forms import TopicForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from .utils import notify_subscribers

def forum_home(request):
    categories = Category.objects.all()
    notifications = []
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'accounts/home.html', {'categories': categories, 'notifications': notifications})

class SubcategoryTopicsView(View):
    def get(self, request, subcategory_id):
        subcategory = get_object_or_404(Subcategory, id=subcategory_id)
        topics = subcategory.topics.all()
        form = TopicForm()
        notifications = []
        if request.user.is_authenticated:
            notifications = Notification.objects.filter(user=request.user, is_read=False)
        return render(request, 'accounts/subcategory_topics.html', {
            'subcategory': subcategory,
            'topics': topics,
            'form': form,
            'notifications': notifications
        })

    @method_decorator(login_required)
    def post(self, request, subcategory_id):
        subcategory = get_object_or_404(Subcategory, id=subcategory_id)
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.subcategory = subcategory
            topic.author = request.user
            topic.save()
            Subscription.objects.get_or_create(user=request.user, topic=topic)
            return redirect('subcategory_topics', subcategory_id=subcategory.id)
        topics = subcategory.topics.all()
        notifications = []
        if request.user.is_authenticated:
            notifications = Notification.objects.filter(user=request.user, is_read=False)
        return render(request, 'accounts/subcategory_topics.html', {
            'subcategory': subcategory,
            'topics': topics,
            'form': form,
            'notifications': notifications
        })

@method_decorator(login_required, name='dispatch')
class TopicDetailView(View):
    def get(self, request, topic_id):
        topic = get_object_or_404(Topic, id=topic_id)
        comments = topic.comments.all()
        form = CommentForm()
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        can_delete_any_comment = request.user.has_perm('accounts.can_delete_any_comment')
        return render(request, 'accounts/topic_detail.html', {
            'topic': topic,
            'comments': comments,
            'form': form,
            'can_delete_any_comment': can_delete_any_comment,
            'notifications': notifications
        })

    @method_decorator(login_required)
    def post(self, request, topic_id):
        topic = get_object_or_404(Topic, id=topic_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.topic = topic
            comment.author = request.user
            comment.save()
            notify_subscribers(comment)
            Subscription.objects.get_or_create(user=request.user, topic=topic)
            return redirect('topic_detail', topic_id=topic.id)
        comments = topic.comments.all()
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        can_delete_any_comment = request.user.has_perm('accounts.can_delete_any_comment')
        return render(request, 'accounts/topic_detail.html', {
            'topic': topic,
            'comments': comments,
            'form': form,
            'can_delete_any_comment': can_delete_any_comment,
            'notifications': notifications
        })

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author and not request.user.groups.filter(name='admin').exists():
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('topic_detail', topic_id=comment.topic.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'accounts/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author and not request.user.has_perm('accounts.can_delete_any_comment'):
        return HttpResponseForbidden()

    if request.method == 'POST':
        comment.delete()
        return redirect('topic_detail', topic_id=comment.topic.id)

    return render(request, 'accounts/delete_comment.html', {'comment': comment})

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'accounts/notifications.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    if notification.user == request.user:
        notification.is_read = True
        notification.save()
    return redirect('notifications')
