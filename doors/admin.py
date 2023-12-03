from django.contrib import admin
from .models import Product,Category,Category_1

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['title','slug']
    prepopulated_fields = {'slug':['title']}

@admin.register(Category)
class AdminProduct(admin.ModelAdmin):
    #list_display = ['title','slug']
    #prepopulated_fields = {'slug':['title']}
    pass

@admin.register(Category_1)
class AdminProduct(admin.ModelAdmin):
    #list_display = ['title','slug']
    #prepopulated_fields = {'slug':['title']}
    pass
# Register your models here.
