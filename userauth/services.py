from django.contrib.auth import get_user_model

User = get_user_model()
def create_user(username, email, password):
    user = User.objects.create_user(username=username, email=email, password=password)
    # Additional logic if needed
    return user
