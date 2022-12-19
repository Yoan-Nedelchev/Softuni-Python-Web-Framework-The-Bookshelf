from django.forms import ModelForm

from theBookshelf.book.models import BookReview


class EditReviewForm(ModelForm):
    class Meta:
        model = BookReview
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super(EditReviewForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control border border-warning'
