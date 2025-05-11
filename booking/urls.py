from django.urls import path
from . import views
from .views import movie_schedule
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('book/<int:movie_id>/', views.book_ticket, name='book_ticket'),
    path('movie/<int:movie_id>/schedule/', movie_schedule, name='movie_schedule'),
]