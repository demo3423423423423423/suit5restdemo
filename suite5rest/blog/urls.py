from django.urls import path
from . import views

urlpatterns = [
    path('writers/', views.writer_list),
    path('writer/<int:pk>', views.writer_detail),
    path('writer/<int:writer_pk>/article/<int:article_pk>', views.writer_article_action),
    path('writer/<int:writer_pk>/articles/', views.writer_article_action),
    path('writer/<int:writer_pk>/article/<int:article_pk>/blog/<int:blog_pk>', views.writer_blog_action),
    path('articles/', views.article_list),
    path('article/<int:pk>', views.article_detail),
    path('blogs/', views.blog_list),
    path('blog/<int:pk>', views.blog_detail),
    path('blog/<int:blog_pk>/articles', views.blog_article_action),
]