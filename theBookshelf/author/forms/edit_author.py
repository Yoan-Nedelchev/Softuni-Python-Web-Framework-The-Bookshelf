from django.core.exceptions import ValidationError
from django.forms import ModelForm
from theBookshelf.author.models import Author


class EditAuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'genre', 'photo', 'biography']

    def __init__(self, *args, **kwargs):
        super(EditAuthorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if visible.auto_id == 'id_genre':
                visible.field.disabled = True

    def clean_first_name(self):
        if self.cleaned_data['first_name'].strip() == '':
            raise ValidationError('Title cannot be blank!')

        return self.cleaned_data['first_name']

    def clean_last_name(self):
        if self.cleaned_data['last_name'].strip() == '':
            raise ValidationError('Last name cannot be blank!')
        return self.cleaned_data['last_name']

    def clean_genre(self):
        if self.cleaned_data['genre'] == None or self.cleaned_data['genre'] == '' or self.instance.genre != self.cleaned_data['genre']:
            raise ValidationError(
                'Attempted author genre change.')
        return self.cleaned_data['genre']

    def clean_photo(self):
        if self.cleaned_data['photo'].strip() == '':
            raise ValidationError('Please, choose a photo!')
        return self.cleaned_data['photo']

    def clean_biography(self):
        if self.cleaned_data['biography'].strip() == '':
            raise ValidationError('Biography cannot be blank!')
        return self.cleaned_data['biography']
