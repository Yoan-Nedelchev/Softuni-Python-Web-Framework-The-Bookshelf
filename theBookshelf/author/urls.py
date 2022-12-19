from django.urls import path, include

from theBookshelf.author.views import author_genres, ListAuthorsView, CreateAuthorView, DetailsAuthorView, \
    EditAuthorView, DeleteAuthorView

urlpatterns = (
    path('add/', CreateAuthorView.as_view(), name='add author'),
    path('genres/', include([
        path('', author_genres, name='author genres'),
        path('<str:genre>', ListAuthorsView.as_view(), name='filtered author list'),
    ])),
    path('author/<int:pk>/', include([
        path('', DetailsAuthorView.as_view(), name='details author'),
        path('edit/', EditAuthorView.as_view(), name='edit author'),
        path('delete/', DeleteAuthorView.as_view(), name='delete author'),
    ]))
)
