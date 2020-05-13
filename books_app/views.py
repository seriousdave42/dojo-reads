from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Author, Book, Review
from login_app.models import User

def books_home(request):
    if "user_name" not in request.session:
        messages.error(request, "Please log in!")
        return redirect('/')
    context = {
        "user_name" : request.session["user_name"],
        "recent_reviews" : Review.objects.all().order_by("-created_at")[:3],
        "books" : Book.objects.all()
    }
    return render(request, 'home.html', context)

def add_book(request):
    if "user_name" not in request.session:
        messages.error(request, "Please log in!")
        return redirect('/')
    context = {
        "author_list" : Author.objects.all()
    }
    return render(request, 'add_book.html', context)

def new_book(request):
    errors = Book.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books/add_book')
    errors = Review.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books/add_book')
    if request.POST["author_id"] == "-1":
        author = Author.objects.create(
            name = request.POST["new_author"]
        )
    else:
        author = Author.objects.get(id = request.POST["author_id"])
    book = Book.objects.create(
        title = request.POST["title"],
        author = author
    )
    Review.objects.create(
        rating = request.POST["rating"],
        review_text = request.POST["review_text"],
        book = book,
        user = User.objects.get(id = request.session["user_id"])
    )
    return redirect(f'/books/{book.id}')

def book_page(request, book_id):
    if "user_name" not in request.session:
        messages.error(request, "Please log in!")
        return redirect('/')
    context = {
        "book" : Book.objects.get(id = book_id),
        "reviews" : Review.objects.filter(book = book_id, user = request.session["user_id"]),
        "user_id" : request.session["user_id"]
    }
    return render(request, 'book.html', context)

def new_review(request, book_id):
    errors = Review.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/books/{book_id}')
    book = Book.objects.get(id = book_id)
    Review.objects.create(
        rating = request.POST["rating"],
        review_text = request.POST["review_text"],
        book = book,
        user = User.objects.get(id = request.session["user_id"])
    )
    return redirect(f'/books/{book.id}')

def user_page(request, user_id):
    if "user_name" not in request.session:
        messages.error(request, "Please log in!")
        return redirect('/')
    user = User.objects.get(id = user_id)
    context = {
        "user" : user,
        "reviews" : len(user.book_reviews.all())
    }
    return render(request, 'user.html', context)

def delete_review(request, review_id):
    review = Review.objects.get(id = review_id)
    review.delete()
    return redirect(request.META["HTTP_REFERER"])

