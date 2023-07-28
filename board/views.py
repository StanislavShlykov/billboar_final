
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Category, Author, Response
from .filters import PostFilter
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import PostForm, ResponseForm
from django.urls import reverse_lazy
from taskboard.tasks import mail_new, hello, like_mail


# Create your views here.
def content(request):
    hello.delay()
    return render(request, 'flatpages/main.html')

def like(request, pk):
    response = Response.objects.get(id=pk)
    like_mail.delay(pk)
    return render(request, 'like.html', {'response': response})


class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'post_list.html'
    context_object_name = 'news_list'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post - {self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post - {self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Author.objects.get(user=self.request.user)
        return context

class ResponseDetail(DetailView):
    model = Response
    template_name = 'response.html'
    context_object_name = 'response'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Author.objects.get(user=self.request.user)
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def post(self, request, *args, **kwargs):
        if request.FILES:
            post = Post(
                post_name=request.POST['post_name'],
                post_text=request.POST['post_text'],
                author=Author.objects.get(user_id=request.user.id),
                file=request.FILES['file']
            )
        else:
            post = Post(
                post_name=request.POST['post_name'],
                post_text=request.POST['post_text'],
                author=Author.objects.get(user_id=request.user.id),
            )
        post.save()
        category_id = request.POST.getlist('category')
        for cat in category_id:
            post.category.add(Category.objects.get(pk=cat))
        mail_new.delay(post.pk)
        return HttpResponseRedirect('/posts/')

    # def form_valid(self, form):
    #     post = form.save()
    #     mail_new.delay(post.pk)
    #     return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class IndexView(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'protect/index.html'
    context_object_name = 'post_list'


    def get_queryset(self):
        queryset = Post.objects.filter(author__user=self.request.user)
        # self.filterset = PostFilter(self.request.GET, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Author.objects.get(user=self.request.user)
        context['posts'] = Post.objects.filter(author=context['author'])
        # context['filterset'] = self.filterset
        return context

# def personal_page(request):
#     filter_params = request.GET.copy()
#
#     author = Author.objects.get(user=request.user)
#     filtered_posts = Post.objects.filter(author=author)
#     # Настройте пагинацию для отфильтрованного queryset
#     paginator = Paginator(filtered_posts, 2)
#     page_number = request.GET.get('page')  # Получите номер текущей страницы из параметра 'page' в запросе
#     try:
#         articles_page = paginator.page(page_number)
#     except EmptyPage:
#         articles_page = paginator.page(paginator.num_pages)
#
#     return render(request, 'personal_page.html', {
#         'articles_page': articles_page,
#         'filter_params': filter_params,
#         'author': author,
#         'filtered_posts': filtered_posts,
#     })


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class ResponseDelete(DeleteView):
    model = Response
    template_name = 'response_delete.html'
    success_url = reverse_lazy('all_responses')

class ResponseCreate(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'response_edit.html'

    def post(self, request, *args, **kwargs):
        response = Response(
            post=Post.objects.get(id=self.kwargs['pk']),
            user=self.request.user,
            text=request.POST['text'],
        )
        response.save()
        return HttpResponseRedirect('/posts/')

class AllResponseList(LoginRequiredMixin, ListView):
    model = Response
    ordering = '-resp_date'
    template_name = 'response_list_all.html'
    context_object_name = 'response_list'
    paginate_by = 2

class ResponseList(LoginRequiredMixin, ListView):
    model = Response
    ordering = '-resp_date'
    template_name = 'response_list.html'
    context_object_name = 'response_list'
    paginate_by = 2

    def get_queryset(self):
        queryset = Response.objects.filter(post=Post.objects.get(id=self.kwargs['pk']))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(id=self.kwargs['pk'])
        context['author'] = context['post'].author
        context['user'] = self.request.user
        context['responses'] = Response.objects.filter(post=context['post'])
        return context

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     return self.filterset.qs
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filterset'] = self.filterset
    #     return context


def sign_me(request):
    user = request.user
    category = Category.objects.get(cat_name=request.GET['category'])
    category.users.add(user)
    return HttpResponse('вы подписались!')
