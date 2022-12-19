from django.contrib import admin
from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

from theBookshelf.accounts.forms.edit_profile import EditProfileForm
from theBookshelf.accounts.forms.sign_up import SignUpForm
from theBookshelf.accounts.models import Profile
from theBookshelf.book.forms.create_book import CreateBookForm
from theBookshelf.book.forms.edit_book import EditBookForm
from theBookshelf.book.models import Book

UserModel = get_user_model()


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = EditBookForm
    add_form = CreateBookForm
    ordering = ('title',)
    list_display = ['title', 'author', 'genre']
    readonly_fields = ('publication_date_and_time', 'slug', 'creator')
    fieldsets = (
        ('Book Info',
         {'classes': ('collapse-open',),
             'fields': ('title', 'genre', 'author', 'cover_photo',  'description')
          }),
        ('Additional Info',
         {'classes': ('collapse',),
          'fields': ('slug', 'publication_date_and_time', 'creator')
          }),
    )
    add_fieldsets = (
        ('Add Book', {
            'classes': ('wide',),
            'fields': ('username', 'genre', 'cover_photo', 'description'),
        }),
    )
