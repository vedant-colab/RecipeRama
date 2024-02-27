from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('blog_view', views.blog_view, name='blog_view'),
    path('create_blog', views.create_blog, name='create_blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('search/', views.search_view, name='search_view'),
    path('delete_blog/<slug:slug>/', views.delete_blog, name='delete_blog'),
]