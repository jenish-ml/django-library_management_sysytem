from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import MemberRegistrationForm, UserRoleForm
from .models import User
from Books.models import Borrow
from django.contrib.admin.views.decorators import staff_member_required


def register(request):
    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'MEMBER'
            user.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = MemberRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('book_list')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    user = request.user
    borrowed_books = Borrow.objects.filter(member=user, return_date__isnull=True)
    return render(request, 'profile.html', {'user': user, 'borrowed_books': borrowed_books})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user.email = request.POST.get('email', user.email)
        user.save()
        return redirect('profile')
    return render(request, 'edit_profile.html', {'user': user})


@staff_member_required  
def manage_users(request):
    users = User.objects.all()
    if request.method == 'POST':
        pass
    return render(request, 'manage_users.html', {'users': users})

