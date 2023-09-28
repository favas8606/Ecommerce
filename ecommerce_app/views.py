from django.shortcuts import get_object_or_404, render
from .models import Products, Category
from django.core.paginator import Paginator, EmptyPage, InvalidPage

def index(request):
    return render(request, 'index.html')
#  First page , getting slug and dtails
def allProdCat(request, c_slug=None):
    c_page = None
    product_list = None

    if c_slug is not None:
        c_page = get_object_or_404(Category, slug=c_slug)
        product_list = Products.objects.filter(catogery=c_page, available=True)
    else:
        product_list = Products.objects.filter(available=True)
    
    paginator = Paginator(product_list, 3)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request, 'category.html', {'catogery': c_page, 'products': products})

#  For product details

def productDetails(request, c_slug, product_slug):
    try:
        product = Products.objects.get(catogery__slug = c_slug, slug = product_slug)
    except Exception as e:
        raise e
    
    return render(request, 'product.html',{'product':product})