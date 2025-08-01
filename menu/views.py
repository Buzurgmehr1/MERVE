from django.shortcuts import render
from django.views import generic

from django.db.models import Q
from .models import Product, Category
# Create your views here.


class ProductListView(generic.ListView):
    model = Product
    template_name = 'menu/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.select_related('category')
        category_id = self.request.GET.get('category')
        search_query = self.request.GET.get('q')

        if category_id:
            queryset = queryset.filter(category__id=category_id)

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        context['search_query'] = self.request.GET.get('q', '')
        return context



class CategoryListView(generic.ListView):
    model = Category
    context_object_name = 'category'