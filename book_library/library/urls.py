from django.urls import path
from .views import index, signup, dashboard, user_logout

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', user_logout, name='logout'),
]