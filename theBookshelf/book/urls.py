from django.urls import path, include

from theBookshelf.book.views import CreateBookView, book_genres, ListBooksView, DetailsBookView, EditBookView, \
    DeleteBookView, LikeBookView, AddReviewView, DeleteReviewView, EditReviewView

urlpatterns = (
    path('add/', CreateBookView.as_view(), name='add book'),
    path('genres/', include([
        path('', book_genres, name='book genres'),
        path('<str:genre>', ListBooksView.as_view(), name='filtered book list'),
    ])),
    path('book/<slug:slug>/', include([
        path('', DetailsBookView.as_view(), name='details book'),
        path('like/', LikeBookView.as_view(), name='like book'),
        path('comment/', include([
            path('', AddReviewView.as_view(), name='comment book'),
            path('edit/<int:pk>', EditReviewView.as_view(), name='edit review'),
            path('delete/<int:pk>', DeleteReviewView.as_view(), name='delete review')
        ])),
        path('edit/', EditBookView.as_view(), name='edit book'),
        path('delete/', DeleteBookView.as_view(), name='delete book'),
    ])),
)
