from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, UserLoginForm
from .models import Book, BorrowedBook, Donation

def index(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'index.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = UserLoginForm()
    return render(request, 'index.html', {'form': form})

def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('index')
    
    books = Book.objects.all()
    
    if request.method == "POST":
        book_id = request.POST.get('book_id')
        action_type = request.POST.get('action_type')
        
        if action_type == 'borrow':
            book = Book.objects.get(id=book_id)
            if book.available_copies > 0:
                BorrowedBook.objects.create(user=request.user, book=book)
                book.available_copies -= 1
                book.save()
        
        elif action_type == 'return':
            borrowed_book = BorrowedBook.objects.get(user=request.user, book__id=book_id)
            borrowed_book.delete()
            book.available_copies += 1
            book.save()

        elif action_type == 'donate':
            title = request.POST.get('donation_title')
            author_name = request.POST.get('donation_author')
            Donation.objects.create(user=request.user, book_title=title, author_name=author_name)

        return redirect('dashboard')

    return render(request, 'dashboard.html', {'books': books})

def user_logout(request):
    logout(request)
    return redirect('index')