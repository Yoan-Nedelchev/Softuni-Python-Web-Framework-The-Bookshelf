from django.core.exceptions import ValidationError
from django.forms import ModelForm
from theBookshelf.common.models import Feedback


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_title(self):
        if self.cleaned_data['title'].strip() == '':
            raise ValidationError('Title cannot be blank!')
        return self.cleaned_data['title']

    def clean_content(self):
        if self.cleaned_data['content'].strip() == '':
            raise ValidationError('Plase, fill in your feedback!')
        return self.cleaned_data['content']

