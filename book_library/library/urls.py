from django.urls import path
from .views import (index, signup, dashboard, user_logout, available_books, borrow_books, donate_books, user_profile, readers_club)

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', user_logout, name='logout'),
    path('available-books/', available_books, name='available_books'),  # New URL for available books
    path('borrow-books/', borrow_books, name='borrow_books'),          # New URL for borrowing books
    path('donate-books/', donate_books, name='donate_books'),          # New URL for donating books
    path('user-profile/', user_profile, name='user_profile'),          # New URL for user profile
    path('readers-club/', readers_club, name='readers_club'),         # New URL for book readers club
]