
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from blogs.models import BlogPost


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            role = form.cleaned_data['role']
            user_group, created = Group.objects.get_or_create(name=role)
            user.groups.add(user_group)

            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def is_author(user):
    return user.groups.filter(name='Author').exists()


@login_required
@user_passes_test(is_author)
def author_dashboard(request):
    posts = BlogPost.objects.filter(
        author=request.user
    ).select_related('category').order_by('-created_at')

    return render(
        request,
        'accounts/author_dashboard.html',
        {'posts': posts}
    )


@login_required
def dashboard_redirect(request):
    user = request.user

    if user.is_superuser or user.is_staff:
        return redirect('pending_posts')

    elif user.groups.filter(name='Author').exists():
        return redirect('author_dashboard')

    else:
        return redirect('blog_list')
