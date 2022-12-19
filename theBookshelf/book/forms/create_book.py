from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.text import slugify

from theBookshelf.book.models import Book


class CreateBookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'cover_photo', 'description']

    def __init__(self, *args, **kwargs):
        super(CreateBookForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_title(self):
        if self.cleaned_data['title'].strip() == '':
            raise ValidationError('Title cannot be blank!')

        slug_cleaned = slugify(self.cleaned_data['title'])
        if Book.objects.filter(slug=slug_cleaned).exists():
            raise ValidationError('There already is a book with the same title!')

        return self.cleaned_data['title']

    def clean_author(self):
        print(self.cleaned_data['author'])
        if self.cleaned_data['author'] == None:
            raise ValidationError(
                'Please, choose an author! If the author is not in the list, please add an author first!')
        return self.cleaned_data['author']

    def clean_genre(self):
        if self.cleaned_data['genre'] == '':
            raise ValidationError(
                'Please, choose a genre!')
        return self.cleaned_data['genre']

    def clean_cover_photo(self):
        if self.cleaned_data['cover_photo'].strip() == '':
            raise ValidationError('Please, choose a cover photo!')
        return self.cleaned_data['cover_photo']

    def clean_description(self):
        if self.cleaned_data['description'].strip() == '':
            raise ValidationError('Description cannot be blank!')
        return self.cleaned_data['description']

    def clean(self):
        cleaned_data = super().clean()
        genre = cleaned_data.get("genre")
        author = cleaned_data.get("author")

        if genre and author and genre not in author.genre:
            raise ValidationError(
                "Book genre and author genre must be the same."
            )
