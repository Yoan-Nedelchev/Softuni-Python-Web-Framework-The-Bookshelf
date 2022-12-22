from django.core.exceptions import ValidationError
from theBookshelf.book.forms.create_book import CreateBookForm


class EditBookForm(CreateBookForm):
    def __init__(self, *args, **kwargs):
        super(EditBookForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            # if visible.auto_id == 'id_genre':
            #     visible.field.disabled = True
            # elif visible.auto_id == 'id_author':
            #     visible.field.disabled = True

    def clean_title(self):
        if self.cleaned_data['title'].strip() == '':
            raise ValidationError('Title cannot be blank!')
        return self.cleaned_data['title']
