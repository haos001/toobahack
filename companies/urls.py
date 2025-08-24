from django.urls import path
from . import views

urlpatterns = [
    path('', views.company_list, name='company_list'),
    path('company/<int:pk>/', views.company_detail, name='company_detail'),
    path('apply/', views.company_apply, name='company_apply'),
    path('apply/success/', views.apply_success, name='apply_success'),
]