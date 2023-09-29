from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    disc = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(upload_to='catogery', blank=True)
    

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

        # for getting url

    def get_url(self):
        return reverse('ecommerce_app:products_by_category',  args=[(self.slug)])

        # setting proper name

    def __self__(self):
        return '{}'.format(self.name)


class Products(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    desc = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    catogery = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product', blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default= False)
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now= True)
    
    def get_url(self):
        return reverse('ecommerce_app:prodCatDetail', args=[self.catogery.slug, self.slug])
    

    class Meta:
        # db_table = 'Products'
        ordering =  ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'



    def __str__(self):
        return '{}'.format(self.name)