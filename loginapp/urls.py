from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_training_menu, name='vulns'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('search-user/', views.search_user, name='sql_injection'),
    path('search/', views.search_page, name='search'),
    path('sensitive_data_exposure/', views.cryptographic_failures, name='sensitive_data_exposure'),
    path('hardcoded_secrets/', views.hardcoded_secrets, name='hardcoded_secrets'),
    path('hardcoded_secrets/js/hardcoded.js', views.hardcoded_secrets_js, name='javascript_file'),
    path('swagger/', views.exposed_swagger, name='swagger'),
    path('swagger-file/', views.exposed_swagger_file, name='swagger-file'),
    path('xss/', views.displayed_xss, name='xss'),
    path('id/', views.sql_injection, name='check_id'),
    path('administrator/', views.get_admin_page, name='admin'),
    path('user/<int:user_id>/', views.user_details, name='user_details'),
]

