from django.conf.urls.static import static
from django.urls import path

from catalog.views import *
from skypro_online_store import settings

urlpatterns = [
    path('', main_menu, name='main_menu'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('contact_us/', contact_us, name='contact_us'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('create_product', ProductCreateView.as_view(), name='product_create'),
    path('update_product/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('product_delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
