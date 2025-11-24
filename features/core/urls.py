
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='home'),            # root -> index
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/', views.home, name='home'),         # separate home url
]
