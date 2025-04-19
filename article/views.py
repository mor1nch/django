from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from article.models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'

    def get_queryset(self):
        return Article.objects.filter(is_published=True)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'

    def get_object(self, *args):
        self.object = super().get_object(*args)
        self.object.views += 1
        self.object.save()
        return self.object


class ArticleCreateView(CreateView):
    model = Article
    fields = ('title', 'body', 'preview')
    success_url = reverse_lazy('article-list')
    template_name = 'article_create.html'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title.lower())
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ('title', 'body', 'preview')
    template_name = 'article_create.html'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title.lower())
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article-detail', args=[self.object.slug])


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('article-list')
    template_name = 'article_confirm_delete.html'
