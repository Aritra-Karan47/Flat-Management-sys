from django.urls import path
from . import views

urlpatterns = [
    path('', views.complaint_list, name='complaint_list'),
    path('create/', views.CreateComplaintView.as_view(), name='complaint_create'),
    path('<int:pk>/', views.complaint_detail, name='complaint_detail'),
    path('<int:pk>/upvote/', views.upvote_complaint, name='upvote_complaint'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
]