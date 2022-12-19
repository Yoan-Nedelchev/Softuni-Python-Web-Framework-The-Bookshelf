from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class News(models.Model):
    header = models.CharField(
        null=False,
        blank=False,
        max_length=50
    )
    title = models.CharField(
        null=False,
        blank=False,
        max_length=50
    )

    content = models.TextField(
        null=False,
        blank=False,
    )

    publication_date_and_time = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=False,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '{}. {}| {}'.format(self.pk, self.header, self.title)

    class Meta:
        ordering = ('-publication_date_and_time',)
        verbose_name_plural = "news"


class Feedback(models.Model):
    title = models.CharField(
        null=False,
        blank=True,
        max_length=50
    )

    content = models.TextField(
        null=False,
        blank=True,
    )

    submission_date_and_time = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=False,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '{}| {}'.format(self.title, self.user)

    class Meta:
        ordering = ('-submission_date_and_time',)
        verbose_name_plural = "feedback"
