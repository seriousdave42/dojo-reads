from django.db import models
# from datetime import datetime, timedelta
from login_app.models import User
# from django.utils import timezone

class Author(models.Model):
    name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class BookManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data["title"]) <= 0:
            errors["title"] = "Title is required!"
        if post_data["author_id"] == "-1" and len(post_data["new_author"]) <= 0:
            errors["title"] = "Author name is required"
        return errors
        
class Book(models.Model):
    title = models.CharField(max_length = 255)
    author = models.ForeignKey(Author, related_name = "books_written", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BookManager()

class ReviewManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['review_text']) > 0 and len(post_data['review_text']) < 10:
            errors['title'] = "Review must be at least ten characters"
        return errors
        
class Review(models.Model):
    rating = models.SmallIntegerField()
    review_text = models.TextField()
    book = models.ForeignKey(Book, related_name = "user_reviews", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name = "book_reviews", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ReviewManager()