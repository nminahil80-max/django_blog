from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import BlogPostForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import BlogPost
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Category
from django.views.decorators.http import require_POST

def is_author(user):
    return user.groups.filter(name='Author').exists()


@login_required
@user_passes_test(is_author)
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('author_dashboard')
    else:
        form = BlogPostForm()

    return render(request, 'blogs/post_form.html', {'form': form})
@login_required
@user_passes_test(is_author)
def edit_post(request, post_id):
    post = get_object_or_404(
        BlogPost,
        id=post_id,
        author=request.user,
        status__in=[
            BlogPost.Status.DRAFT,
            BlogPost.Status.REJECTED
        ]
    )

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect('author_dashboard')
    else:
        form = BlogPostForm(instance=post)

    return render(request, 'blogs/post_form.html', {'form': form})
@login_required
@user_passes_test(is_author)
def delete_post(request, post_id):
    post = get_object_or_404(
        BlogPost,
        id=post_id,
        author=request.user,
        status__in=[
            BlogPost.Status.DRAFT,
            BlogPost.Status.REJECTED
        ]
    )

    if request.method == 'POST':
        post.delete()
        return redirect('author_dashboard')

    return HttpResponse("Confirm deletion")

@login_required
@user_passes_test(is_author)
@require_POST
def submit_post(request, post_id):
    post = get_object_or_404(
        BlogPost,
        id=post_id,
        author=request.user,
        status__in=[
            BlogPost.Status.DRAFT,
            BlogPost.Status.REJECTED
        ]
    )

    post.status = BlogPost.Status.PENDING
    post.submitted_at = timezone.now()
    post.rejection_reason = ''
    post.save()

    return redirect('author_dashboard')

def blog_list(request):
    posts = BlogPost.objects.filter(
        status=BlogPost.Status.PUBLISHED
    ).select_related('author', 'category').order_by('-created_at')

    search_query = request.GET.get('search', '')
    category_slug = request.GET.get('category', '')

    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    categories = Category.objects.all()

    return render(request, 'blogs/blog_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_slug': category_slug,
    })
    
def blog_detail(request, slug):
    post = get_object_or_404(
        BlogPost.objects.select_related('author', 'category'),
        slug=slug,
        status=BlogPost.Status.PUBLISHED
    )

    comments = post.comments.select_related('user').order_by('-created_at')
    total_likes = post.likes.count()

    return render(request, 'blogs/blog_detail.html', {
        'post': post,
        'comments': comments,
        'total_likes': total_likes,
    })