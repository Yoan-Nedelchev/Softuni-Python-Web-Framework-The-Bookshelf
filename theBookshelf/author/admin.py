from django.contrib import admin
from theBookshelf.author.forms.add_author import AddAuthorForm
from theBookshelf.author.forms.edit_author import EditAuthorForm
from theBookshelf.author.models import Author


class AuthorAdmin(admin.ModelAdmin):
    form = EditAuthorForm
    add_form = AddAuthorForm
    ordering = ('-publication_date_and_time',)
    list_display = ['first_name', 'last_name', 'genre']
    readonly_fields = ('publication_date_and_time', 'creator')
    fieldsets = (
        ('Author Info',
         {'classes': ('collapse-open',),
          'fields': ('first_name', 'last_name', 'genre', 'photo', 'biography')
          }),
        ('Additional Info',
         {'classes': ('collapse',),
          'fields': ('publication_date_and_time', 'creator')
          }),
    )
    add_fieldsets = (
        ('Add Author', {
            'fields': ('first_name', 'last_name', 'genre', 'photo', 'biography'),
        }),
    )


admin.site.register(Author, AuthorAdmin)
