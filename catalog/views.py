from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product, Version


def main_menu(request):
    return render(request, 'main_menu.html')


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products_with_versions = []
        for product in context['products']:
            active_version = Version.objects.filter(product=product, current_version=True).first()

            products_with_versions.append({
                'product': product,
                'active_version': active_version,
            })

        context['products_with_versions'] = products_with_versions
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    template_name = 'product_create.html'


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_create.html'

    def get_success_url(self):
        return reverse('product_detail', args=[self.object.id])


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')
    template_name = 'product_confirm_delete.html'


def contact_us(request):
    return render(request, 'contact_us.html')
