from django.shortcuts import render

# Create your views here.
from ecommerce_app.models import Products
from django.db.models import Q

def SearchResult(request):
    products = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        products = Products.objects.all().filter(Q( name__contains = query) | Q(desc__contains = query))
    return render(request, 'search.html', {'query':query, 'products':products})