from django.test import TestCase
from django.urls import reverse
from django.test import Client

from theBookshelf.accounts.models import AppUser
from theBookshelf.author.models import Author
from theBookshelf.book.forms.create_book import CreateBookForm
from theBookshelf.book.models import Book


class AccountsTestCase(TestCase):
    username = 'davinci'
    email = 'doncho@minkov.it'
    password = '123'

    def setUp(self):
        self.client = Client()
        self.user = AppUser.objects.create(username=self.username, email=self.email, password=self.password)
        self.user.set_password('123')
        self.user.save()

    def assertListEmpty(self, ll):
        return self.assertListEqual([], ll, 'The list is not empty')

    def test_form_submit_book_with_different_genre_than_author(self):
        author = Author(
            first_name="Ivan",
            last_name="Ivanov",
            genre="Mystery",
            photo="https://www.standoutbooks.com/wp-content/uploads/2013/11/Author-Profile-Picture-3.jpg?ezimgfmt=rs:234x350/rscb4/ngcb4/notWebP",
            biography="Ivan's biography",
            creator=self.user,
        )
        author.save()

        form = CreateBookForm(data={
            "title": "New book",
            "genre": "Romance",
            "cover_photo": "https://www.standoutbooks.com/wp-content/uploads/2013/11/Author-Profile-Picture-3.jpg?ezimgfmt=rs:234x350/rscb4/ngcb4/notWebP",
            "description": "New book's description",
            "creator": self.user,
            "author": author
        })

        print(form.errors)
        self.assertEqual(
            form.errors["__all__"],
            ["Book genre and author genre must be the same."]
        )

    def test_book_like_correctly_recorded_and_updated_in_book_instance(self):
        author = Author(
            first_name="Ivan",
            last_name="Ivanov",
            genre="Mystery",
            photo="https://www.standoutbooks.com/wp-content/uploads/2013/11/Author-Profile-Picture-3.jpg?ezimgfmt=rs:234x350/rscb4/ngcb4/notWebP",
            biography="Ivan's biography",
            creator=self.user,
        )
        author.save()

        book = Book(
            title="New book",
            genre="Mystery",
            cover_photo="https://www.standoutbooks.com/wp-content/uploads/2013/11/Author-Profile-Picture-3.jpg?ezimgfmt=rs:234x350/rscb4/ngcb4/notWebP",
            description="New book's description",
            creator=self.user,
            author=author
        )
        book.save()

        self.client.force_login(self.user)

        self.assertEqual(0, book.number_of_likes)

        response = self.client.get(reverse('like book', kwargs={
            'slug': book.slug,
        }), follow=True)

        self.assertEqual(1, response.context['book'].number_of_likes)

