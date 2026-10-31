from django.urls import path
from . import views

urlpatterns = [
    path(
        'pending-posts/', views.pending_posts, name='pending_posts'
    ),

    path(
        'approve/<int:post_id>/', views.approve_post, name='approve_post'
    ),

    path(
        'reject/<int:post_id>/', views.reject_post, name='reject_post'
    ),
]