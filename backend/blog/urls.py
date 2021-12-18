from django.urls import path

from .feeds import LatestPostsFeed
from .views import CommentCreate, PostDetailView, PostListView, PostShare

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/', PostListView.as_view(), name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/share/', PostShare.as_view(), name='post_share'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/comment/', CommentCreate.as_view(), name='comment_create'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
]
