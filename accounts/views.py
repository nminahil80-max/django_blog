from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
def register_view(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            user_group, created = Group.objects.get_or_create(name='User')
            user.groups.add(user_group)
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })
    
def is_author(user):
    return user.groups.filter(name='Author').exists()

@login_required
@user_passes_test(is_author)
def author_dashboard(request):
    return HttpResponse("Welcome to Author Dashboard")