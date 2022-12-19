from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from theBookshelf.author.models import Author

UserModel = get_user_model()


class Book(models.Model):
    MAX_TITLE = 100
    GENRE_CHOICES = [
        ('Romance', 'Romance'),
        ('Mystery', 'Mystery'),
        ('Fantasy and Science Fiction', 'Fantasy and Science Fiction'),
        ('Thrillers and Horrors', 'Thrillers and Horrors'),
        ('Young Adult', 'Young Adult'),
        ('Self-help', 'Self-help'),
        ('Biography, Autobiography and Memoir', 'Biography, Autobiography and Memoir'),
        ('Esoteric', 'Esoteric'),
    ]

    number_of_likes = models.IntegerField(
        default=0,
        null=False,
        blank=False
    )

    number_of_reviews = models.IntegerField(
        default=0,
        null=False,
        blank=False
    )

    title = models.CharField(
        max_length=MAX_TITLE,
        null=False,
        blank=True,
    )

    genre = models.CharField(
        max_length=35,
        choices=GENRE_CHOICES,
        blank=True,
        null=False
    )

    cover_photo = models.URLField(
        null=False,
        blank=True,
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    creator = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    publication_date_and_time = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=False,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f'{self.title}')
        return super().save(*args, **kwargs)

    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=False)

    def __str__(self):
        return '{} by {}'.format(self.title, self.author.full_name)

    class Meta:
        ordering = ('-publication_date_and_time',)


class Like(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)


class BookReview(models.Model):
    content = models.TextField(
        null=True,
        blank=True,
    )

    publication_date_and_time = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=False,
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-publication_date_and_time',)
