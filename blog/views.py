from django.shortcuts import render,get_object_or_404, redirect
from datetime import datetime
from .models import Blog
from userauth.models import Profile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.
def blog_view(request):
    '''View the blog posts'''
    blog_posts = Blog.objects.order_by('-created_at')
    paginator = Paginator(blog_posts, per_page=4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog.html', {'page_obj': page_obj, 'blog_posts':blog_posts})

@login_required(login_url="/userauth/login")
def create_blog(request):
    '''This is view is used to create blog posts'''
    if request.method == 'POST':
        user = request.user  # Get the current user
        profile = Profile.objects.get(user=user)  # Get the profile instance related to the user
        author = profile
        title = request.POST.get('title')
        content = request.POST.get('content')
        created_at = datetime.today()
        updated_at = datetime.today()

        blog = Blog(author=author,title=title,content=content,created_at=created_at,updated_at=updated_at)
        blog.save()
    return render(request, 'create_blog.html')

def blog_detail(request, slug):
    '''Viewing the indepth of the blog posts'''
    blog_post = get_object_or_404(Blog, slug=slug) #getting the blog post of the matching slug
    return render(request, 'blog_detail.html', {'blog_post': blog_post})


def search_view(request):
    '''Handles the search query from user to fetch blogs '''
    query = request.GET.get('q')
    if query:
        blogs = Blog.objects.filter(title__icontains=query)
    else:
        blogs = Blog.objects.all()

    context = {
        'blogs': blogs,
        'query': query,
        }

    return render(request, 'search_results.html', context)

@login_required
def delete_blog(request, slug):
    '''Handles the deleting of the blogs'''
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_view')

    return render(request, 'delete_blog_confirmation.html', {'blog': blog})
