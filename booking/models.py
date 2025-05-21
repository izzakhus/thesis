from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField("Название фильма", max_length=255)
    description = models.TextField("Описание")
    duration = models.PositiveIntegerField("Длительность (мин)")
    poster = models.ImageField("Постер", upload_to='posters/', blank=True, null=True)
    genres = models.CharField("Жанры", max_length=255)
    rating = models.DecimalField("Рейтинг", max_digits=3, decimal_places=1, default=0.0)
    country = models.CharField(max_length=100, default='Не указано', verbose_name='Страна')
    studio = models.CharField(max_length=100, default='Студия не указана', verbose_name='Студия')
    budget = models.PositiveIntegerField(default=0, verbose_name="Бюджет ($)", help_text="Укажите бюджет в долларах")
    director = models.CharField(max_length=100, default='Режиссёр не указан', verbose_name='Режиссёр')
    actor = models.CharField(max_length=100, default='Не указано', verbose_name='Актеры')

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def __str__(self):
        return self.title


class MovieFrame(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='frames')
    image = models.ImageField(upload_to='movie_frames/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Кадр из {self.movie.title}"


class CinemaHall(models.Model):
    name = models.CharField("Название", max_length=100)
    rows = models.PositiveIntegerField("Рядов")
    seats_per_row = models.PositiveIntegerField("Мест в ряду")
    address = models.CharField("Адрес", max_length=255, blank=True, null=True)
    metro_station = models.CharField("Станция метро", max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Кинозал"
        verbose_name_plural = "Кинозалы"

    def __str__(self):
        return f"{self.name} ({self.rows}x{self.seats_per_row})"


class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Фильм")
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, verbose_name="Кинозал")
    start_time = models.DateTimeField("Начало сеанса")

    class Meta:
        verbose_name = "Сеанс"
        verbose_name_plural = "Сеансы"

    def __str__(self):
        return f"{self.movie.title} — {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class Seat(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name="Сеанс")
    row = models.PositiveIntegerField("Ряд")
    number = models.PositiveIntegerField("Место")
    is_reserved = models.BooleanField("Зарезервировано", default=False)

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        status = "Занято" if self.is_reserved else "Свободно"
        return f"{self.session.movie.title} | Ряд: {self.row} Место: {self.number} ({status})"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, verbose_name="Место")
    booked_at = models.DateTimeField("Дата бронирования", auto_now_add=True)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"{self.user.username} забронировал {self.seat} в {self.booked_at.strftime('%d.%m.%Y %H:%M')}"
