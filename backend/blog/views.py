from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.edit import CreateView

from .forms import CommentForm, PostShareForm
from .models import Comment, Post


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
        url = post.get_absolute_url()
        post.url = self.request.build_absolute_uri(url)
        self.success_url = url
        form.send_mail(post)
        return super().form_valid(form)

    def get_object(self):
        return get_object_or_404(Post, slug=self.kwargs['post'],
                                 status='published',
                                 publish__year=self.kwargs['year'],
                                 publish__month=self.kwargs['month'],
                                 publish__day=self.kwargs['day'])


class CommentCreate(SuccessMessageMixin, FormView):
    template_name = 'blog/post_comment.html'
    form_class = CommentForm
    success_message = 'Comment added successfully!'

    def form_valid(self, form):
        post = self.get_object()
        self.success_url = post.get_absolute_url()
        form.instance.post = post
        form.save()
        return super().form_valid(form)

    def get_object(self):
        return get_object_or_404(Post, slug=self.kwargs['post'],
                                 status='published',
                                 publish__year=self.kwargs['year'],
                                 publish__month=self.kwargs['month'],
                                 publish__day=self.kwargs['day'])
