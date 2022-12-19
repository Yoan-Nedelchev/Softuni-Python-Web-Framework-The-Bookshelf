from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

UserModel = get_user_model()


class Author(models.Model):
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

    first_name = models.CharField(
        max_length=20,
        null=False,
        blank=True,
    )

    last_name = models.CharField(
        max_length=20,
        null=False,
        blank=True,
    )

    genre = models.CharField(
        max_length=35,
        choices=GENRE_CHOICES,
        null=False,
        blank=True,
    )

    photo = models.URLField(
        null=False,
        blank=True,
    )

    biography = models.TextField(
        null=False,
        blank=True,
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
    )

    creator = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    publication_date_and_time = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=False,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f'{self.first_name} {self.last_name}')
        return super().save(*args, **kwargs)

    def __str__(self):
        return '{}. {} {} | {}'.format(self.pk, self.first_name, self.last_name, self.genre)

    class Meta:
        ordering = ('-publication_date_and_time',)

    @property
    def full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name
