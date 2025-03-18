from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.models import User
from .models import UserProfile
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from .models import User

# Dummy credentials for the purpose of training
valid_username = 'admin'
valid_password = 'password123'

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

         # Vulnerability 1: Reveals if a user exists
        print(User.objects.all)
        if not User.objects.filter(username=username).exists():
            error = "User does not exist."
        else:
            # Vulnerability 2: No rate limiting or account lockout
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Vulnerability 3: Logs in without additional checks (e.g., 2FA)
                login(request, user)
                return redirect('home')  # Redirect to a dummy home page
            else:
                error = "Incorrect password."
    
    return render(request, 'login.html', {'error': error})


def broken_access_control(request):
    if request.user.is_authenticated:
        username = request.GET.get('username', '')
        try:
            user_profile = UserProfile.objects.get(user__username=username)
            return render(request, 'training/broken_access_control.html', {
                'user_profile': user_profile
            })
        except UserProfile.DoesNotExist:
            return render(request, 'training/broken_access_control.html', {
                'error': "User profile not found."
            })
    else:
        return HttpResponse("You need to log in to access this page.")
    
def sql_injection(request):
    user_input = request.GET.get('id')
    query = f"SELECT * FROM auth_user WHERE id = {user_input}"  # Unsanitized
    cursor = connection.cursor()
    cursor.execute(query)
    return HttpResponse("Query executed")
    
def cryptographic_failures(request):
    # Simulate retrieving all users with their MD5 hashed passwords
    users = User.objects.all()

    return render(request, 'cryptographic_failures.html', {'users': users})

def hardcoded_secrets(request):
    return render(request, 'hardcoded.html')

def exposed_swagger(request):
    return render(request, 'swagger.json')

def displayed_xss(request):
    return render(request, 'XSS.html')

def exposed_credentials(request):
    # Expose database credentials (DO NOT DO THIS IN PRODUCTION)
    db_config = {
        'ENGINE': settings.DATABASES['default']['ENGINE'],
        'NAME': settings.DATABASES['default']['Clients'],
        'USER': settings.DATABASES['default']['major2025'],
        'PASSWORD': settings.DATABASES['default']['propect123#!'],
        'HOST': settings.DATABASES['default']['izuri.vitafluence.com'],
        'PORT': settings.DATABASES['default']['5000'],
    }
    return JsonResponse(db_config)


def get_admin_page(request):
    return render(request, 'admin.html')

def get_training_menu(request):
    return render(request, 'menu.html')

def hardcoded_secrets_js(request):
    return render(request, 'js/hardcoded.js')

def user_details(request, user_id):
    # Fetch the user by ID without any authorization check (IDOR vulnerability)
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user_details.html', {'user': user})


def search_user(request):
    query = request.GET.get('query', '')
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM auth_user WHERE username = '{query}'")  # Vulnerable query
        row = cursor.fetchone()
    return HttpResponse(f"User: {row}")

# Search for a user (SQL Injection): http://127.0.0.1:8000/training/search-user/?query=test' OR '1'='1

def search_page(request):
    return render(request, 'search.html')


def home(request):
    return render(request, 'home.html')