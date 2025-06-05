from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/create/', views.report_create, name='report_create'),
    path('reports/<int:pk>/', views.report_detail, name='report_detail'),
    path('reports/<int:pk>/edit/', views.report_edit, name='report_edit'),
    path('reports/<int:pk>/delete/', views.report_delete, name='report_delete'),
] 