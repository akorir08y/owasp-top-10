from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('search-user/', views.search_user, name='sql_injection'),
    path('search/', views.search_page, name='search'),
    path('sensitive_data_exposure/', views.cryptographic_failures, name='sensitive_data_exposure'),
    path('hardcoded_secrets/', views.hardcoded_secrets, name='hardcoded_secrets'),
    path('hardcoded_secrets/js/hardcoded.js', views.hardcoded_secrets_js, name='javascript_file'),
    path('swagger/', views.exposed_swagger, name='swagger'),
    path('xss/', views.displayed_xss, name='xss'),
    path('id/', views.sql_injection, name='check_id'),
    path('administrator/', views.get_admin_page, name='admin'),
    path('vulns/', views.get_training_menu, name='vulns'),
    path('user/<int:user_id>/', views.user_details, name='user_details'),
]

