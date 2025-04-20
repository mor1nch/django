from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product, Version
from catalog.services import get_categories


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
        context['categories'] = get_categories()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    template_name = 'product_create.html'
    permission_required = [
        'catalog.can_change_description',
        'catalog.can_change_category',
        'catalog.can_change_is_published'
    ]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        user = self.request.user

        if user.groups.filter(name='manager').exists():
            allowed_fields = ['description', 'category', 'is_published']
            form.fields = {key: form.fields[key] for key in allowed_fields if key in form.fields}

        return form


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_create.html'
    permission_required = [
        'catalog.can_change_description',
        'catalog.can_change_category',
        'catalog.can_change_is_published'
    ]

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user

        is_owner = product.owner == user
        is_manager = user.groups.filter(name='manager').exists()
        is_superuser = user.is_superuser

        if not (is_owner or is_manager or is_superuser):
            return HttpResponseForbidden("У вас нет прав для редактирования этого продукта.")

        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        is_superuser = user.is_superuser

        if (user.groups.filter(name='manager').exists() or is_superuser) and self.object.owner != user:
            allowed_fields = ['description', 'category', 'is_published']
            form.fields = {key: form.fields[key] for key in allowed_fields if key in form.fields}

        return form

    def get_success_url(self):
        return reverse('product_detail', args=[self.object.id])


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')
    template_name = 'product_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        product = self.get_object()

        context['is_owner'] = product.owner == user
        context['is_manager'] = user.groups.filter(name='manager').exists()
        return context


def contact_us(request):
    return render(request, 'contact_us.html')
