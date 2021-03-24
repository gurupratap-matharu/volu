from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.detail import SingleObjectMixin

from .forms import PostShareForm
from .models import Post


class PostListView(ListView):
    model = Post
    context_object_name = 'post_list'
    queryset = Post.published.all()
    paginate_by = 12


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    extra_context = {'form': PostShareForm()}

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, slug=self.kwargs['post'],
                                 status='published',
                                 publish__year=self.kwargs['year'],
                                 publish__month=self.kwargs['month'],
                                 publish__day=self.kwargs['day'])
        return post


class PostShare(SingleObjectMixin, FormView):
    form_class = PostShareForm

    def form_valid(self, form):
        post = self.get_object()
        post.url = self.request.build_absolute_uri(post.get_absolute_url())
        form.send_mail(post)
        return super().form_valid(form)

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, slug=self.kwargs['post'],
                                 status='published',
                                 publish__year=self.kwargs['year'],
                                 publish__month=self.kwargs['month'],
                                 publish__day=self.kwargs['day'])
        return post

    def get_success_url(self) -> str:
        return self.get_object().get_absolute_url()
