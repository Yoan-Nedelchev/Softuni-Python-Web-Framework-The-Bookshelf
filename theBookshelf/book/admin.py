from django.contrib import admin
from theBookshelf.book.forms.create_book import CreateBookForm
from theBookshelf.book.forms.edit_book import EditBookForm
from theBookshelf.book.models import Book


class BookAdmin(admin.ModelAdmin):
    form = EditBookForm
    add_form = CreateBookForm
    ordering = ('title',)
    list_display = ['title', 'author', 'genre']
    readonly_fields = ('publication_date_and_time', 'slug', 'creator')
    fieldsets = (
        ('Book Info',
         {'classes': ('collapse-open',),
          'fields': ('title', 'genre', 'author', 'cover_photo', 'description')
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


admin.site.register(Book, BookAdmin)
