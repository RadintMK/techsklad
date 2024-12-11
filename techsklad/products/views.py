# products/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Product
from django.db.models import Q

def home(request):
    categories = Category.objects.all()[:6]
    featured_products = Product.objects.filter(available=True)[:8]
    return render(request, 'products/home.html', {
        'categories': categories,
        'featured_products': featured_products
    })

def catalog(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    search_query = request.GET.get('search', '')
    category_slug = request.GET.get('category', '')
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products/catalog.html', {
        'categories': categories,
        'page_obj': page_obj,
        'search_query': search_query,
        'category_slug': category_slug
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products
    })
    
def stores(request):
    return render(request, 'products/stores.html')

def delivery(request):
    return render(request, 'products/delivery.html')

def contacts(request):
    return render(request, 'products/contacts.html')