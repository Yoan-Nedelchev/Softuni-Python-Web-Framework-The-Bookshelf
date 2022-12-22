from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.db.models import Q, Max, Count
from django.urls import reverse_lazy
from django.views.generic import CreateView

from theBookshelf.author.models import Author
from theBookshelf.book.models import Book, Like
from theBookshelf.common.forms.feedback_form import FeedbackForm
from theBookshelf.common.models import News, Feedback


def index(request):
    books = Book.objects.all()[:3]
    news = News.objects.all()

    context = {
        'books': books,
        'news': news,
    }
    return render(request, 'common/index.html', context)


def search(request):
    def search_authors(data):
        authors_found = Author.objects.all()
        for string in data.split():
            authors_found = authors_found.filter(
                Q(first_name__icontains=string) | Q(last_name__icontains=string))
        return authors_found

    if request.method == 'POST':
        data = request.POST['content']

        authors_found = search_authors(data)
        books_found = Book.objects.filter(title__icontains=data)
        data_found = True
        if not authors_found and not books_found:
            data_found = False

        print(authors_found)
        print(books_found)

        context = {
            'authors_found': authors_found,
            'books_found': books_found,
            'data_found': data_found
        }

        return render(request, 'common/search.html', context)


class CreateFeedbackView(LoginRequiredMixin, CreateView):
    model = Feedback
    success_url = reverse_lazy('index')
    template_name = 'common/feedback.html'
    form_class = FeedbackForm

    def form_valid(self, form):
        feedback = form.save(commit=False)
        feedback.user = self.request.user
        feedback.save()
        return super().form_valid(form)


def about_us(request):
    return render(request, 'common/about_us.html')


def statistics(request):
    max_likes_dict = Book.objects.aggregate(Max('number_of_likes'))
    max_likes = max_likes_dict['number_of_likes__max']
    books_with_max_likes = Book.objects.filter(number_of_likes=max_likes)

    max_reviews_dict = Book.objects.aggregate(Max('number_of_reviews'))
    max_reviews = max_reviews_dict['number_of_reviews__max']
    books_with_max_reviews = Book.objects.filter(number_of_reviews=max_reviews)

    context = {
        'books_max_likes': books_with_max_likes,
        'books_max_reviews': books_with_max_reviews,
        'max_likes': max_likes,
        'max_reviews': max_reviews
    }
    return render(request, 'common/statistics.html', context)


def page_not_found(request, exception):
    return render(request, 'common/404.html')
