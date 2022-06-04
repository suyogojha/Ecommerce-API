from django.db import models
from django.utils.text import slugify
# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True, max_length=200)
    image = models.ImageField(upload_to='images/category', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)
        
        
    def __str__(self):
        return self.category_name
        
      
class QuantityVariant(models.Model):
    variant_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.variant_name
    
class ColorVariant(models.Model):
    color_name = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)
    
    def __str__(self):
        return self.color_name
    
class SizeVariant(models.Model):
    size_name = models.CharField(max_length=100)  
      
    def __str__(self):
        return self.size_name     
        
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField(default=100)
    
    quantity_type = models.ForeignKey(QuantityVariant, null=True, blank=True ,on_delete=models.PROTECT)    
    color_type = models.ForeignKey(ColorVariant, null=True, blank=True ,on_delete=models.PROTECT)
    size_type = models.ForeignKey(SizeVariant, null=True, blank=True ,on_delete=models.PROTECT)
    
    def __str__(self):
        return self.product_name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='images/product/')

