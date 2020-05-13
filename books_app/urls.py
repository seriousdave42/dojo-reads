from django.urls import path
from . import views

urlpatterns = [
    path('', views.books_home),
    path('<int:book_id>', views.book_page),
    path('<int:book_id>/new_review', views.new_review),
    path('reviews/<int:review_id>/delete', views.delete_review),
    path('users/<int:user_id>', views.user_page),
    path('add_book', views.add_book),
    path('new_book', views.new_book)
]
