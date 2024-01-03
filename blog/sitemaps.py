from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):

    changefreq = 'weekly' #показ. частоту обнов. страниц статей
    priority = 0.9 # степень их совпадений с тематикой сайта

    def items(self): #метод возврашает статьи которые будут в карте сайта
        return Post.objects.all()

    def lastmod(self,obj): #метод возврашает данные когда были обналениы статьи полученный выше
        return obj.date_update