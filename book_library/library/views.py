from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, UserLoginForm
from .models import Book, BorrowedBook, Donation
from django.core.paginator import Paginator

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
    
    # Fetch available books
    available_books = Book.objects.all()
    
    # Fetch borrowed books for the logged-in user
    borrowed_books = BorrowedBook.objects.filter(user=request.user)
    
    # Fetch donated books for the logged-in user
    donated_books = Donation.objects.filter(user=request.user)

    # Handle POST requests for borrowing, returning, or donating books
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
            borrowed_books = BorrowedBook.objects.filter(user=request.user, book__id=book_id)
            if borrowed_books.exists():
                # If there are multiple records, delete all of them
                for borrowed_book in borrowed_books:
                    borrowed_book.delete()
                    book = borrowed_book.book  # Get the book instance from borrowed_book
                    book.available_copies += 1
                    book.save()

        elif action_type == 'donate':
            title = request.POST.get('donation_title')
            author_name = request.POST.get('donation_author')
            Donation.objects.create(user=request.user, book_title=title, author_name=author_name)

        return redirect('dashboard')

    # Implement pagination for available books
    page_number = request.GET.get('page')
    paginator = Paginator(available_books, 5)  # Show 5 books per page
    available_books_page = paginator.get_page(page_number)

    context = {
        'available_books': available_books_page,
        'borrowed_books': borrowed_books,
        'donated_books': donated_books,
    }
    
    return render(request, 'dashboard.html', context)

def user_logout(request):
    logout(request)
    return redirect('index')

def available_books(request):
    # Logic to retrieve and display available books
    return render(request, 'available_books.html')

def borrow_books(request):
    # Logic to handle borrowing books
    return render(request, 'borrow_books.html')

def return_books(request):
    # Logic to handle borrowing books
    return render(request, 'return_books.html')

def donate_books(request):
    # Logic to handle donating books
    return render(request, 'donate_books.html')

def user_profile(request):
    # Logic to display user profile information
    return render(request, 'user_profile.html')

def readers_club(request):
    # Logic for book readers club information
    return render(request, 'readers_club.html')