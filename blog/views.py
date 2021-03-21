from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Post


class PostListView(ListView):
    model = Post
    context_object_name = 'post_list'
    queryset = Post.published.all()


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, slug=self.kwargs['post'],
                                 status='published',
                                 publish__year=self.kwargs['year'],
                                 publish__month=self.kwargs['month'],
                                 publish__day=self.kwargs['day'])
        print('veer getting object...')
        print('veer post: {}'.format(post))
        return post
