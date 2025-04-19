from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from catalog.models import Product


def main_menu(request):
    return render(request, 'main_menu.html')


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'


def contact_us(request):
    return render(request, 'contact_us.html')
