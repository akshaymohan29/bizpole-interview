"""
URL configuration for bizpoleproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from boredapi import  views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.register_user, name ='register'),
    path('home/', views.home, name='home'),
    path('edit-activity/<int:activity_id>/', views.edit_activity, name='edit_activity'),
    path('delete-activity/<int:activity_id>/', views.delete_activity, name='delete_activity'),
    path('delete-user/<int:activity_id>/', views.delete_user, name='delete_user'),
    path('fetch-activity/<int:user_id>/', views.fetch_activity, name='fetch_activity'),
    path('user-activities/<int:user_id>/', views.user_activities, name='user-activities'),

]
