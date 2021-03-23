from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from .forms import PostShareForm
from .models import Post


class PostListView(ListView):
    model = Post
    context_object_name = 'post_list'
    queryset = Post.published.all()
    paginate_by = 12


class PostDetailView(FormMixin, DetailView):
    model = Post
    context_object_name = 'post'
    form_class = PostShareForm
    success_message = "Post shared successfully!"

    def get_success_url(self) -> str:
        return self.get_object().get_absolute_url()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, slug=self.kwargs['post'],
                                 status='published',
                                 publish__year=self.kwargs['year'],
                                 publish__month=self.kwargs['month'],
                                 publish__day=self.kwargs['day'])
        return post
