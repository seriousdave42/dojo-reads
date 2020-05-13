from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User

def index(request):
    if "user_id" in request.session:
        return redirect('/books')
    return render(request, 'login.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    User.objects.create(name = request.POST['name'],
        user_name = request.POST['user_name'],
        email = request.POST['email'],
        password = pw_hash)
    messages.success(request, "Successfully registered! Please log in")
    return redirect('/')

def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if not user:
        messages.error(request, "Email not registered")
        return redirect('/')
    logged_user = user[0]
    if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
        request.session['user_id'] = logged_user.id
        request.session['user_name'] = logged_user.user_name
        return redirect('/books')
    else:
        messages.error(request, "Incorrect password!")
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')
