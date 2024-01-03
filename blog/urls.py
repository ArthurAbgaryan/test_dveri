from django.urls import path
from .views import main_list,PostDeleteView, post_detail,PostUpdateView,create_post,save_posts,save_posts_ajax,like_post_ajax
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap
from .feeds import PostFeed

sitemaps = {'posts':PostSitemap,}

urlpatterns = [
    path('', main_list, name = 'main_list'),
    path('tag/<slug:tag_slug>/', main_list, name='main_list_tag'),
    path('sitemap.xml',sitemap, {'sitemaps':sitemaps}, name ='django.contrib.sitemaps.views.sitemap' ),
    path('lasted_feed/',PostFeed(), name = 'feed_blog'),
    path('blog/<slug:slug>/<int:pk>/detail/',post_detail,name = 'post_detail'),
    path('blog/<int:pk>/delete/',PostDeleteView.as_view(), name = 'post_delete'),
    path('blog/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('blog/create/', create_post, name='post_create'),
    path('blog/saves_post/',save_posts, name = 'saves_posts'),
    path('blog/save_post_ajax/',save_posts_ajax, name = 'save_ajax'),
    path('blog/like_post_ajax/', like_post_ajax, name='like_ajax')

]
