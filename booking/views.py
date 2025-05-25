from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Session, Booking, CinemaHall
from .forms import BookingForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import random


def index(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'movie_list.html', context)


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    other_movies = Movie.objects.exclude(id=movie.id)
    other_movies = list(other_movies)
    random.shuffle(other_movies)
    other_movies = other_movies[:3]

    context = {
        'movie': movie,
        'other_movies': other_movies,
    }
    return render(request, 'movie_detail.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'register.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Неверные данные для входа.')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')

    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def movie_schedule(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    sessions = Session.objects.filter(movie=movie).select_related('hall').only(
        'hall__name', 'hall__address', 'hall__metro_station', 'start_time'
    )

    schedules = [{
        'cinema_name': session.hall.name,
        'address': session.hall.address or "Адрес не указан",
        'metro': session.hall.metro_station or "Метро не указано",
        'showtimes': [session.start_time.strftime("%H:%M")],
        'hall_id': session.hall.id
    } for session in sessions]

    return render(request, 'movie_schedule.html', {
        'schedules': schedules,
        'movie': movie
    })


def profile(request):
    return render(request, 'profile.html')
