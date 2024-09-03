from timeit import default_timer
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Product, Order


class ShopIndexView(ListView):
    template_name = 'shopapp/shop-index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["time_running"] = default_timer()
        return context


class GroupsListView(ListView):
    model = Group
    template_name = 'shopapp/groups-list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('permissions')


class ProductListView(ListView):
    model = Product
    template_name = 'shopapp/products-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return super().get_queryset().filter(archived=False)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shopapp/product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse_lazy('shopapp:products-list')
        context['update_url'] = reverse_lazy('shopapp:product-update', kwargs={'pk': self.object.pk})
        context['archive_url'] = reverse_lazy('shopapp:product-archive', kwargs={'pk': self.object.pk})
        return context


class ProductCreateView(CreateView):
    model = Product
    template_name = 'shopapp/product-form.html'
    fields = '__all__'
    success_url = reverse_lazy('shopapp:products-list')


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'shopapp/product-form.html'
    fields = '__all__'
    success_url = reverse_lazy('shopapp:products-list')


class ProductArchiveView(DeleteView):
    model = Product
    template_name = 'shopapp/product-archive.html'
    fields = ['archived']
    success_url = reverse_lazy('shopapp:products-list')


class OrderListView(ListView):
    model = Order
    template_name = 'shopapp/orders-list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return super().get_queryset().select_related('user').prefetch_related('products')


class OrderDetailView(DetailView):
    model = Order
    template_name = 'shopapp/order-detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse_lazy('shopapp:orders-list')
        context['update_url'] = reverse_lazy('shopapp:order-update', kwargs={'pk': self.object.pk})
        context['delete_url'] = reverse_lazy('shopapp:order-delete', kwargs={'pk': self.object.pk})
        return context


class OrderCreateView(CreateView):
    model = Order
    template_name = 'shopapp/order-form.html'
    fields = '__all__'
    success_url = reverse_lazy('shopapp:orders-list')


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'shopapp/order-form.html'
    fields = '__all__'
    success_url = reverse_lazy('shopapp:orders-list')


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'shopapp/order-delete.html'
    success_url = reverse_lazy('shopapp:orders-list')
