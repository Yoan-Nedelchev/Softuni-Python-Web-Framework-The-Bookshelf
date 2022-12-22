from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from theBookshelf.accounts.models import AppUser, Profile
from theBookshelf.book.forms.create_book import CreateBookForm
from theBookshelf.book.forms.edit_book import EditBookForm
from theBookshelf.book.forms.edit_review import EditReviewForm
from theBookshelf.book.models import Book, Like, BookReview


UserModel = get_user_model()


def book_genres(request):
    return render(request, 'book/book_genres.html')


class ListBooksView(ListView):
    template_name = 'book/filtered_books.html'
    context_object_name = 'books'
    model = Book
    paginate_by = 3

    def get_queryset(self):
        genre = self.kwargs['genre']
        if genre == "romance":
            genre = "Romance"
        elif genre == "mystery":
            genre = "Mystery"
        elif genre == "fantasy-and-science-fiction":
            genre = "Fantasy and Science Fiction"
        elif genre == "thrillers-and-horrors":
            genre = "Thrillers and Horrors"
        elif genre == "young-adult":
            genre = "Young Adult"
        elif genre == "self-help":
            genre = "Self-help"
        elif genre == "biography-autobiography-and-memoir":
            genre = "Biography, Autobiography and Memoir"
        elif genre == "esoteric":
            genre = "Esoteric"
        new_context = Book.objects.filter(genre=genre)
        return new_context


class CreateBookView(LoginRequiredMixin, CreateView):
    model = Book
    success_url = reverse_lazy('index')
    template_name = 'book/create_book.html'
    form_class = CreateBookForm

    def form_valid(self, form):
        book = form.save(commit=False)
        book.creator = self.request.user
        book.save()
        return super().form_valid(form)


class DetailsBookView(LoginRequiredMixin, DetailView):
    template_name = 'book/details_book.html'
    context_object_name = 'book'
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = context['book']

        book.likes_count = book.like_set.count()
        is_owner = book.creator == self.request.user
        is_liked_by_user = book.like_set.filter(user_id=self.request.user.id).exists()
        reviews = book.bookreview_set.filter(book_id=book.pk).all()
        creator_profile = Profile.objects.get(user_id=book.creator_id)
        creator_user = UserModel.objects.get(id=book.creator_id)

        reviews_complete_info = []
        for review in reviews:
            user = UserModel.objects.get(id=review.user_id)
            reviews_complete_info.append({
                'content': review.content,
                'creator': user.username,
                'creation_time': review.publication_date_and_time,
                'review_owner': self.request.user == user,
                'review_id': review.pk,
                'profile': Profile.objects.get(user_id=user.id),
            })
            print(reviews_complete_info)

        context['is_owner'] = is_owner
        context['is_liked'] = is_liked_by_user
        context['reviews_complete_info'] = reviews_complete_info
        context['creator_profile'] = creator_profile
        context['creator_user'] = creator_user
        return context


class EditBookView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = 'book/edit_book.html'
    form_class = EditBookForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = ['Romance', 'Mystery', 'Fantasy and Science Fiction', 'Thrillers and Horrors',
                             'Young Adult', 'Self-help', 'Biography, Autobiography and Memoir', 'Esoteric']
        return context

    def get_success_url(self):
        return reverse_lazy('details book', kwargs={'slug': self.kwargs.get('slug')})


class DeleteBookView(LoginRequiredMixin, DeleteView):
    template_name = 'book/delete_book.html'
    model = Book
    success_url = reverse_lazy('index')


class LikeBookView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        book = Book.objects.get(slug=slug)
        like_object_by_user = book.like_set.filter(user_id=self.request.user.id) \
            .first()
        if like_object_by_user:
            like_object_by_user.delete()

            new_number_of_likes = book.number_of_likes - 1
            updated_values = {'number_of_likes': new_number_of_likes}

            for key, value in updated_values.items():
                setattr(book, key, value)
            book.save()

        else:
            like = Like(
                book=book,
                user=self.request.user,
            )
            like.save()

            new_number_of_likes = book.number_of_likes + 1
            updated_values = {'number_of_likes': new_number_of_likes}

            for key, value in updated_values.items():
                setattr(book, key, value)
            book.save()

        return redirect('details book', book.slug)


class AddReviewView(LoginRequiredMixin, CreateView):
    model = BookReview
    fields = ['content']

    def get_success_url(self):
        return reverse_lazy('details book', kwargs={'slug': self.kwargs.get('slug')})

    template_name = 'book/details_book.html'

    def form_valid(self, form):
        book = Book.objects.get(slug=self.kwargs.get('slug'))

        review = form.save(commit=False)
        review.user_id = self.request.user.id
        review.book_id = book.id
        review.save()

        new_number_of_reviews = book.number_of_reviews + 1
        updated_values = {'number_of_reviews': new_number_of_reviews}

        for key, value in updated_values.items():
            setattr(book, key, value)
        book.save()

        return super().form_valid(form)


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    template_name = 'book/details_book.html'
    model = BookReview

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(slug=self.kwargs.get('slug'))

        new_number_of_reviews = book.number_of_reviews - 1
        updated_values = {'number_of_reviews': new_number_of_reviews}

        for key, value in updated_values.items():
            setattr(book, key, value)
        book.save()
        return super(DeleteReviewView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = Book.objects.get(slug=self.kwargs.get('slug'))
        context['book'] = book
        return context

    def get_success_url(self):
        return reverse_lazy('details book', kwargs={'slug': self.kwargs.get('slug')})


class EditReviewView(LoginRequiredMixin, UpdateView):
    model = BookReview
    template_name = 'book/edit_review.html'
    form_class = EditReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = Book.objects.get(slug=self.kwargs.get('slug'))

        book.likes_count = book.like_set.count()
        is_owner = book.creator == self.request.user
        is_liked_by_user = book.like_set.filter(user_id=self.request.user.id).exists()
        reviews = book.bookreview_set.filter(book_id=book.pk).all()
        creator_profile = Profile.objects.get(user_id=book.creator_id)

        reviews_complete_info = []
        for review in reviews:
            user = UserModel.objects.get(id=review.user_id)
            reviews_complete_info.append({
                'content': review.content,
                'creator': user.username,
                'creation_time': review.publication_date_and_time,
                'review_owner': self.request.user == user,
                'review_id': review.pk,
                'profile': Profile.objects.get(user_id=user.id)
            })

        context['is_owner'] = is_owner
        context['is_liked'] = is_liked_by_user
        context['reviews_complete_info'] = reviews_complete_info
        context['creator_profile'] = creator_profile
        context['book'] = book
        return context

    def get_success_url(self):
        return reverse_lazy('details book', kwargs={'slug': self.kwargs.get('slug')})
