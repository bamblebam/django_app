from django.shortcuts import *
from .models import Post
from django.views.generic import *
from django.contrib.auth.mixins import *
from django.contrib.auth.models import User

def about(request):
    return render(request,'blog/about.html',{'title':'home'})

class PostListView(ListView):
    model=Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class PostDetailView(DetailView):
    model=Post
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','content']
    context_object_name = 'post'

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title','content']
    context_object_name = 'post'

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    context_object_name = 'post'
    success_url = '/'

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False

class UserPostListView(ListView):
    model=Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')