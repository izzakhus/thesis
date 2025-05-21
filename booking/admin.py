from django.contrib import admin
from .models import Movie, CinemaHall, Session, Seat, Booking, MovieFrame


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration')
    search_fields = ('title',)


@admin.register(CinemaHall)
class CinemaHallAdmin(admin.ModelAdmin):
    list_display = ('name', 'rows', 'seats_per_row')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('movie', 'hall', 'start_time')
    list_filter = ('movie', 'start_time')


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('session', 'row', 'number', 'is_reserved')
    list_filter = ('session', 'is_reserved')
    search_fields = ('row', 'number')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'seat', 'booked_at')
    list_filter = ('booked_at',)


class MovieFrameInline(admin.TabularInline):
    model = MovieFrame
    extra = 3


