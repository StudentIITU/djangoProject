from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    # Fix the dealer URLs
    path('dealer/<str:dealer_id>/', views.dealer_details, name='dealer_details'),
    path('dealer/<str:dealer_id>/add_review/', views.add_review, name='add_review'),
]