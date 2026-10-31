from django.shortcuts import render

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from blogs.models import BlogPost
from .models import Like, Comment


@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(
        BlogPost,
        id=post_id,
        status=BlogPost.Status.PUBLISHED
    )

    like, created = Like.objects.get_or_create(
        blog=post,
        user=request.user
    )

    if not created:
        like.delete()

    return redirect('blog_detail', slug=post.slug)

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(
        BlogPost,
        id=post_id,
        status=BlogPost.Status.PUBLISHED
    )

    content = request.POST.get('content', '').strip()

    if content:
        Comment.objects.create(
            blog=post,
            user=request.user,
            content=content
        )

    return redirect('blog_detail', slug=post.slug)