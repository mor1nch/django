from django.urls import path

from article.views import *

urlpatterns = [
    path('articles', ArticleListView.as_view(), name='article-list'),
    path('articles/<str:slug>', ArticleDetailView.as_view(), name='article-detail'),
    path('create_article', ArticleCreateView.as_view(), name='article-create'),
    path('update_article/<str:slug>', ArticleUpdateView.as_view(), name='article-update'),
    path('delete/<str:slug>', ArticleDeleteView.as_view(), name='article-delete'),
]
