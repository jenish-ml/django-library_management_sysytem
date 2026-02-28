from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Book, Category, Borrow
from .forms import BookForm, BorrowForm, CategoryForm
from datetime import date, timedelta

def is_librarian(user):
    return user.is_authenticated and user.role == 'LIBRARIAN'
def is_admin(user):
    return user.is_authenticated and user.role == 'ADMIN'
def is_member(user):
    return user.is_authenticated and user.role == 'MEMBER'

# Book list (public)
def book_list(request):
    books = Book.objects.all()
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    available_only = request.GET.get('available')

    if query:
        books = books.filter(title__icontains=query)
    if category_id:
        books = books.filter(category_id=category_id)
    if available_only:
        books = books.filter(available_copies__gt=0)

    categories = Category.objects.all()
    return render(request, 'book_list.html', {
        'books': books,
        'categories': categories,
    })

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book_detail.html', {'book': book})

# Librarian only
@login_required
def book_add(request):
    if not is_librarian(request.user):
        messages.error(request, 'Not allowed')
        return redirect('book_list')
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form, 'action': 'Add'})

@login_required
def book_edit(request, pk):
    if not is_librarian(request.user):
        messages.error(request, 'Not allowed')
        return redirect('book_list')
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form, 'action': 'Edit'})

@login_required
def book_delete(request, pk):
    if not is_librarian(request.user) and not is_admin(request.user):
        messages.error(request, 'Not allowed')
        return redirect('book_list')
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'book_confirm_delete.html', {'book': book})


@login_required
def issue_book(request, book_pk):
    if not is_member(request.user):
        messages.error(request, 'Only members can borrow books')
        return redirect('book_list')
    book = get_object_or_404(Book, pk=book_pk)
    if book.available_copies < 1:
        messages.error(request, 'No copies available')
        return redirect('book_detail', pk=book_pk)

    if request.method == 'POST':
        due_date = date.today() + timedelta(days=14)  # default 2 weeks
        Borrow.objects.create(
            member=request.user,
            book=book,
            due_date=due_date
        )
        book.available_copies -= 1
        book.save()
        messages.success(request, 'Book borrowed successfully')
        return redirect('profile')
    return render(request, 'issue_book.html', {'book': book})

@login_required
def return_book(request, borrow_pk):
    borrow = get_object_or_404(Borrow, pk=borrow_pk, member=request.user)
    if borrow.return_date is None:
        borrow.return_date = date.today()
        borrow.save()
        borrow.book.available_copies += 1
        borrow.book.save()
        messages.success(request, 'Book returned')
    return redirect('profile')

@login_required
def borrow_list(request):
    if is_librarian(request.user) or is_admin(request.user):
        borrows = Borrow.objects.all().select_related('member', 'book')
    else:
        borrows = Borrow.objects.filter(member=request.user)
    return render(request, 'borrow_list.html', {'borrows': borrows})

@login_required
def category_add(request):
    if not (is_librarian(request.user) or is_admin(request.user)):
        messages.error(request, 'You are not allowed to add categories.')
        return redirect('book_list')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('book_list') 
    else:
        form = CategoryForm()

    return render(request, 'category_form.html', {'form': form, 'action': 'Add'})