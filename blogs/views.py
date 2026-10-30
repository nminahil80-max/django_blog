from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import BlogPostForm


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

    return render(request, 'blogs/create_post.html', {'form': form})