from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('signup',views.signup, name='signup'),
    path('login',views.signin, name='signin'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('logout',views.signout,name='logout'),
    path('view_profile',views.view_profile,name='view_profile'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('view_blogs',views.view_blogs,name='view_blogs'),
    path('blogs/<slug:slug>/', views.blog_detail_view, name='blog_detail'),
    path('blogs/<slug:slug>/edit/', views.edit_blog, name='edit_blog'),
    path('forgot-password', views.forgot_password, name='forgot_password'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_password/done/', views.change_password_done, name='change_password_done'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
]