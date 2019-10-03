# coding=utf-8

from django.shortcuts import render, get_object_or_404
from django.views import generic 

from .models import Product, Category

class ProductListView(generic.ListView):

    queryset = Product.objects.all()
    #model = Product
    template_name = "catalog/product_list.html"
    context_object_name = 'product_list'

product_list = ProductListView.as_view()

class CategoryListView(generic.ListView):
    
    context_object_name = 'product_list'
    template_name = "catalog/category.html"

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['current_category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
        return context

category = CategoryListView.as_view()

def product(request, slug, template_name = "catalog/product.html"):
    product = Product.objects.get(slug=slug)
    context = {
        "product" : product,
    }
    return render(request, template_name, context)
    