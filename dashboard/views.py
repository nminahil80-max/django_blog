
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.http import HttpResponse

from blogs.models import BlogPost
from contact.models import ContactMessage


@login_required
@user_passes_test(lambda user: user.is_staff)
def pending_posts(request):
    posts = BlogPost.objects.filter(
        status=BlogPost.Status.PENDING
    ).select_related('author', 'category')

    return render(
        request,
        'dashboard/pending_posts.html',
        {'posts': posts}
    )


@login_required
@user_passes_test(lambda user: user.is_staff)
@require_POST
def approve_post(request, post_id):
    post = get_object_or_404(
        BlogPost,
        id=post_id,
        status=BlogPost.Status.PENDING
    )

    post.status = BlogPost.Status.PUBLISHED
    post.review_at = timezone.now()
    post.rejection_reason = ''
    post.rejection_at = None
    post.save()

    return redirect('pending_posts')


@login_required
@user_passes_test(lambda user: user.is_staff)
@require_POST
def reject_post(request, post_id):
    post = get_object_or_404(
        BlogPost,
        id=post_id,
        status=BlogPost.Status.PENDING
    )

    reason = request.POST.get('rejection_reason', '').strip()

    print("Received rejection reason:", repr(reason))

    if not reason:
        return HttpResponse("Rejection reason is required.")

    post.status = BlogPost.Status.REJECTED
    post.rejection_reason = reason
    post.review_at = timezone.now()
    post.rejection_at = timezone.now()
    post.save()

    post.refresh_from_db()
    print("Saved rejection reason:", repr(post.rejection_reason))

    return redirect('pending_posts')


@login_required
@user_passes_test(lambda user: user.is_staff)
def contact_messages(request):
    messages = ContactMessage.objects.all().order_by('-created_at')

    return render(
        request,
        'dashboard/contact_messages.html',
        {'contact_messages': messages}
    )
