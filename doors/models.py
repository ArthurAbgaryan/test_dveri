from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length = 100,verbose_name=  'название',
                             db_index=True)
    body = models.TextField(max_length=1000,
                            verbose_name= 'Описание товара',blank= True,
                            null=True )
    praice = models.CharField(max_length=10,
                              verbose_name='Цена')
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE,verbose_name= 'Категория товара',
                                 related_name='category')
    category_1 = models.ForeignKey('Category_1',
                                   on_delete=models.CASCADE,verbose_name='Подкатегория', null=True,
                                   related_name='category_1')
    size = models.CharField(max_length=10, verbose_name = 'Размер')
    maker = models.CharField(max_length=100, verbose_name='Изготовитель')
    matter = models.CharField(max_length=100, verbose_name='Материал изготовления')
    color = models.CharField(max_length=100, verbose_name='Цвет')
    image = models.ImageField()
    slug = models.SlugField(max_length=100)
    code = models.CharField(max_length=20, verbose_name='Артикул')
    save_product = models.ManyToManyField(User,related_name= 'save_producte' )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


doors_style = [('steel','метал'),('wood','дерево'),('furniture','фурнитура')]
wood_style = [('laminat','ламинат'),('ekospon','экошпон'),('pvh','ПВХ')]

class Category(models.Model):

    title = models.CharField(max_length=100, choices= wood_style)
    model = models.CharField(max_length=100)

class Category_1(models.Model):

    title = models.CharField(max_length=100, choices= doors_style)
    model = models.CharField(max_length=100)





# Create your models here.
