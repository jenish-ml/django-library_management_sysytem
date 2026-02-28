from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/add/', views.book_add, name='book_add'),
    path('book/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('book/<int:book_pk>/issue/', views.issue_book, name='issue_book'),
    path('borrow/<int:borrow_pk>/return/', views.return_book, name='return_book'),
    path('borrows/', views.borrow_list, name='borrow_list'),
    path('category/add/', views.category_add, name='category_add'),
]