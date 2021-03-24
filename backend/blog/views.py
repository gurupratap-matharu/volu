from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, FormView, ListView

from .forms import CommentForm, PostShareForm
from .models import Post


class PostListView(ListView):
    model = Post
    context_object_name = 'post_list'
    queryset = Post.published.all()
    paginate_by = 12


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, slug=self.kwargs['post'],
                                 status='published',
                                 publish__year=self.kwargs['year'],
                                 publish__month=self.kwargs['month'],
                                 publish__day=self.kwargs['day'])
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(active=True)
        context['comment_form'] = CommentForm()
        return context


class PostShare(SuccessMessageMixin, FormView):
    template_name = 'blog/post_share.html'
    form_class = PostShareForm
    success_message = 'Post shared successfully!'

    def form_valid(self, form):
        post = self.get_object()
        post.url = self.request.build_absolute_uri(post.get_absolute_url())
        self.success_url = post.get_absolute_url()
        form.send_mail(post)
        return super().form_valid(form)

    def get_object(self):
        return get_object_or_404(Post, slug=self.kwargs['post'],
                                 status='published',
                                 publish__year=self.kwargs['year'],
                                 publish__month=self.kwargs['month'],
                                 publish__day=self.kwargs['day'])
