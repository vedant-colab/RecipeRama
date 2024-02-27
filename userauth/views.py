from django.shortcuts import render,redirect, get_object_or_404
from .services import create_user
from .models import Profile, User
from blog.models import Blog
from django.contrib.auth import authenticate, login,logout, update_session_auth_hash
from django.db.utils import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.views import blog_detail
from django.utils import timezone
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from RecipeRecommendation import settings
from django.core.mail import send_mail
# Create your views here.

def signup(request):
    '''The sign up view that processes the sign up of user into the application'''
    error = False #default error 
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            # To create a new user with a unique username
            user = create_user(username=username,email=email,password=password)
            login(request,user)
            return redirect('/userauth/dashboard')
        except IntegrityError:
            error=True #The username already exists in the database, as it should be unique the error is True
    return render(request,r'signup.html', {"error":error})

def signin(request):
    '''Processes the sign in functionality of the web application'''
    if request.method == 'POST':
        # Handle login form submission
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None: #if user exists
            login(request, user)
            return redirect('/userauth/dashboard')  # Redirect to the dashboard view
        
        else:
            messages.error(request, 'Invalid username or password.')
        
    return render(request,'login.html')

@login_required
def dashboard(request):
    ''''Deals with the dashboard presentation '''
    return render(request, 'dashboard.html')

@login_required
def edit_profile(request):
    '''To handle the profile updation process'''
    user = request.user

    # Check if the user has a profile
    if not hasattr(user, 'profile'):
        # Create a new profile for the user
        profile = Profile(user=user)
        profile.save()

    # Fetch the user's existing profile details
    profile = user.profile
    name = profile.name
    bio = profile.bio
    location = profile.country
    dob = profile.dob

    if request.method == 'POST':
        # Handle form submission and update user profile
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        location = request.POST.get('location')
        dob = request.POST.get('dob')

        # Update the user's profile with the new information
        profile.name = name
        profile.bio = bio
        profile.country = location
        profile.dob = dob
        profile.save()

        return redirect('/userauth/view_profile')

    return render(request, 'edit_profile.html', {
        'name': name,
        'bio': bio,
        'location': location,
        'dob': dob,
    })

@login_required
def view_profile(request):
    '''Handles the functionality for user to view it's profile'''
    user = request.user
    return render(request, 'view_profile.html', {'user':user})

@login_required
def view_blogs(request):
    '''Handles the functionality for user to view it's blogs'''
    blogs = Blog.objects.filter(author__user=request.user)
    return render(request,'view_blogs.html', {'blogs': blogs})

@login_required
def signout(request):
    '''The logout implementation of the user'''
    if request.method == 'POST':
        logout(request)
        print(request.user)
        return redirect('/')

def blog_detail_view(request,slug):
    return blog_detail(request,slug)

@login_required
def edit_blog(request,slug):
    '''Used to edit and update the existing blog post '''
    blog_post = get_object_or_404(Blog, slug=slug)

    if request.method == 'POST':
    # Retrieve the updated values from the form
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Update the blog post with the new values
        blog_post.title = title
        blog_post.content = content
        blog_post.save()

        # Update the updated_at field with the current timestamp
        blog_post.updated_at = timezone.now()
        blog_post.save()

        # Redirect to the blog detail page or any other desired page
        return redirect('blog_detail', slug=blog_post.slug)

    return render(request, 'edit_blog.html', {'blog_post': blog_post})

def forgot_password(request):
    '''The functionality to handle the situation if a user forget's it's password'''
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Generate a secure unique token 
            token = default_token_generator.make_token(user)
            user.profile.reset_password_token = token 
            user.profile.save()

            # Send the reset Link to the user's email 
            reset_link = f"{request.scheme}://{request.get_host()}/userauth/reset-password/{token}/"
            subject = 'Reset your Password'
            message = f'Click the following link to reset your password: {reset_link}'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]
            send_mail(subject, message, from_email, to_email, fail_silently=False)
            messages.success(request, 'Password reset link sent to your email. Please check your inbox')
            return redirect('/userauth/login')
        
        else:
            messages.error(request, 'User with this email does not exist')

    return render(request, 'forgot_password.html')


@login_required
def change_password(request):
    '''Handles the changing password for user'''
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) #continues the session of current user
            messages.success(request, 'Your Password was updated successfully!')
            return redirect('change_password_done')
        else:
            messages.error(request,'Please correct the errors below')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def change_password_done(request):
    '''Post html page after user has changed the password'''
    return render(request, 'accounts/change_password_done.html')

def reset_password(request, token):
    '''To handle the reset password form'''
    user = get_object_or_404(User, profile__reset_password_token = token)
    if request.method == 'POST':
        password = request.POST.get('password')
        user.set_password(password)
        user.profile.reset_password_token = None 
        user.profile.save()
        user.save()
        messages.success(request, 'Password reset sucessful. You can now login with your new password')
        return redirect('login')

    return render(request, 'reset_password.html')