from django.contrib.auth.decorators import login_required
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


@login_required
def buy_ticket(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    sessions = Session.objects.filter(movie=movie)

    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        session = get_object_or_404(Session, id=session_id)

        return redirect('confirmation')

    context = {'movie': movie, 'sessions': sessions}
    return render(request, 'buy_ticket.html', context)


@login_required
def book_ticket(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            seats = form.cleaned_data['seats']
            Booking.objects.create(user=request.user, movie=movie, seats=seats)
            return redirect('profile')  # или куда-то ещё
    else:
        form = BookingForm()

    context = {'form': form, 'movie': movie}
    return render(request, 'book_ticket.html', context)


from django.shortcuts import render
from .models import Movie, Session


def movie_schedule(request, movie_id):
    movie = Movie.objects.get(id=movie_id)


    sessions = Session.objects.filter(movie=movie).select_related('hall')

    schedules = []
    for session in sessions:
        schedules.append({
            'cinema_name': session.hall.name,
            'address': "Адрес кинотеатра",
            'metro': "Станция метро",
            'showtimes': [session.start_time.strftime("%H:%M")]
        })

    return render(request, 'movie_schedule.html', {'schedules': schedules})


def profile(request):
    return render(request, 'profile.html')
