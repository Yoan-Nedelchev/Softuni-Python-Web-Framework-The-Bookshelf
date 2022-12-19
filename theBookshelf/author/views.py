from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify

from theBookshelf.accounts.models import Profile
from theBookshelf.author.forms.add_author import AddAuthorForm
from theBookshelf.author.forms.edit_author import EditAuthorForm
from theBookshelf.author.models import Author
from django.views.generic import DetailView, CreateView, FormView, ListView, UpdateView, DeleteView

from theBookshelf.book.models import Book


def author_genres(request):
    return render(request, 'author/author_genres.html')


class ListAuthorsView(ListView):
    template_name = 'author/filtered_authors.html'
    context_object_name = 'authors'
    model = Author
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
        new_context = Author.objects.filter(genre=genre)
        return new_context


class CreateAuthorView(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AddAuthorForm
    success_url = reverse_lazy('index')
    template_name = 'author/create_author.html'

    def form_valid(self, form):
        author = form.save(commit=False)
        author.creator = self.request.user
        author.save()
        return super().form_valid(form)


class EditAuthorView(LoginRequiredMixin, UpdateView):
    model = Author
    template_name = 'author/edit_author.html'
    form_class = EditAuthorForm

    def get_success_url(self):
        return reverse_lazy('details author', kwargs={'pk': self.kwargs.get('pk')})


class DetailsAuthorView(LoginRequiredMixin, DetailView):
    template_name = 'author/details_author.html'
    context_object_name = 'author'
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = context['author']

        is_owner = author.creator == self.request.user
        books = Book.objects.filter(author_id=author.id)
        creator_profile = Profile.objects.get(user_id=author.creator_id)

        genre_slug = slugify(author.genre)
        context['is_owner'] = is_owner
        context['books'] = books
        context['creator_profile'] = creator_profile
        context['genre_slug'] = genre_slug

        return context


class DeleteAuthorView(LoginRequiredMixin, DeleteView):
    template_name = 'author/delete_author.html'
    model = Author
    success_url = reverse_lazy('index')
