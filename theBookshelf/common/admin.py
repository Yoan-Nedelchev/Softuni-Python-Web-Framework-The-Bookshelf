from django.contrib import admin
from theBookshelf.common.forms.create_news import CreateNewsForm
from theBookshelf.common.models import News, Feedback


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'header', 'content', 'publication_date_and_time', 'user']
    ordering = ['title']
    add_form = CreateNewsForm
    fieldsets = (
        ('Header', {
            'fields': ('header',),
        }),
        ('Other info', {
            'fields': ('title', 'content')
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


admin.site.register(News, NewsAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'user']
    ordering = ['title']


admin.site.register(Feedback, FeedbackAdmin)
