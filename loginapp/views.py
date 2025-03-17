from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.models import User
from .models import UserProfile
from django.http import JsonResponse
from django.conf import settings

# Dummy credentials for the purpose of training
valid_username = 'admin'
valid_password = 'password123'

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # **Insecure Password Storage and SQL Injection**
        # Vulnerable check directly against hardcoded credentials
        # **Unsafe: This can be exploited via SQL injection**
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM auth_user WHERE username = '{username}' AND password = '{password}'")
        user = cursor.fetchall()

        if username == valid_username and password == valid_password:
            return HttpResponse(f"Login successful! Welcome, {username}")
        else:
            # **Cross-Site Scripting (XSS) vulnerability** 
            # The username is displayed directly, which could allow XSS attacks.
            return HttpResponse(f"Login failed! Invalid username or password. <br> {username}")
    
    return render(request, 'login.html')


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

from django.shortcuts import render, get_object_or_404
from .models import User

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