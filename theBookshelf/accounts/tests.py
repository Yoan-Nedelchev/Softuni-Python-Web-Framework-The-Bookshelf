from django.test import TestCase
from django.urls import reverse
from django.test import Client
from theBookshelf.accounts.forms.login import LoginForm
from theBookshelf.accounts.forms.sign_up import SignUpForm
from theBookshelf.accounts.models import Profile, AppUser
from theBookshelf.author.models import Author
from theBookshelf.book.models import Book


class AccountsTestCase(TestCase):
    username = 'davinci'
    email = 'davinci@gmail.com'
    password = '123'

    def setUp(self):
        self.client = Client()
        self.user = AppUser.objects.create(username=self.username, email=self.email, password=self.password)
        self.user.set_password('123')
        self.user.save()

    def assertListEmpty(self, ll):
        return self.assertListEqual([], ll, 'The list is not empty')

    def test_AppUser_model(self):
        app_user = AppUser.objects.create(username='dido', email='dido@abv.bg', password='123')
        self.assertTrue(isinstance(app_user, AppUser))
        self.assertEqual(app_user.username, 'dido')

    def test_profile_created_upon_user_creation(self):
        """Animals that can speak are correctly identified"""
        app_user = AppUser.objects.create(username='dido', email='dido@abv.bg', password='123')
        profile = Profile.objects.get(user_id=app_user.pk)
        self.assertEqual(app_user.profile.pk, profile.user_id)

    def test_login_form_wrong_password(self):
        app_user = AppUser.objects.create(username='dido', email='dido@abv.com', password='123')
        form = LoginForm(data={"username": "davinci", "password": "12"})

        self.assertEqual(
            form.errors["__all__"],
            ["Please enter a correct username and password. Note that both fields may be case-sensitive."]
        )

    def test_signup_form_different_passwords(self):
        form = SignUpForm(
            data={"username": "davinci", "email": "davinci@davinci.com", "password1": "123", "password2": "12"})

        self.assertEqual(
            form.errors["password2"],
            ["The two password fields didn’t match."]
        )

    def test_signup_form_submit_empty(self):
        form = SignUpForm(
            data={"username": "", "email": "", "password1": "", "password2": ""})

        self.assertEqual(
            form.errors["username"],
            ["This field is required."]
        )

        self.assertEqual(
            form.errors["email"],
            ["This field is required."]
        )

        self.assertEqual(
            form.errors["password1"],
            ["This field is required."]
        )

        self.assertEqual(
            form.errors["password2"],
            ["This field is required."]
        )

    def test_view_successful_login(self):
        author = Author(
            first_name='Pepe',
            last_name='Damon',
            genre='Mystery',
            photo='https://images.pexels.com/photos/3772623/pexels-photo-3772623.jpeg?cs=srgb&dl=pexels-andrea-piacquadio-3772623.jpg&fm=jpg',
            biography='Jamie Damon\'s biography',
            creator=self.user,
        )
        author.save()

        book = Book(
            title='Cooking Book',
            genre='Mystery',
            cover_photo='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1284431932l/8253037.jpg',
            description='Cook Book Description',
            creator=self.user,
            author_id=author.id
        )
        book.save()

        second_book = Book(
            title='Second book',
            genre='Mystery',
            cover_photo='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1284431932l/8253037.jpg',
            description='Cook Book Description',
            creator=self.user,
            author_id=author.id
        )
        second_book.save()

        third_book = Book(
            title='Third book',
            genre='Mystery',
            cover_photo='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1284431932l/8253037.jpg',
            description='Cook Book Description',
            creator=self.user,
            author_id=author.id
        )
        third_book.save()

        app_user = AppUser.objects.create(username='dido', email='dido@abv.com', password='123')
        app_user.set_password('123')
        app_user.save()

        response = self.client.post('/accounts/sign-in/', {'username': self.user.username, 'password': '123'}, follow=True)
        print(response.context['user'])

    def test_profile_page_with_no_authors_and_books(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('details profile', kwargs={
            'pk': self.user.pk,
        }), follow=True)

        print(response.context)
        self.assertEqual(self.user.id, response.context['profile'].user_id)
        self.assertListEmpty(list(response.context['authors_created']))
        self.assertListEmpty(list(response.context['books_posted']))

    def test_profile_page_with_book(self):
        author = Author(
            first_name='Pepe',
            last_name='Damon',
            genre='Mystery',
            photo='https://images.pexels.com/photos/3772623/pexels-photo-3772623.jpeg?cs=srgb&dl=pexels-andrea-piacquadio-3772623.jpg&fm=jpg',
            biography='Jamie Damon\'s biography',
            creator=self.user,
        )
        author.save()

        book = Book(
            title='Cooking Book',
            genre='Mystery',
            cover_photo='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1284431932l/8253037.jpg',
            description='Cook Book Description',
            creator=self.user,
            author_id=author.id
        )
        book.save()

        second_book = Book(
            title='Second book',
            genre='Mystery',
            cover_photo='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1284431932l/8253037.jpg',
            description='Cook Book Description',
            creator=self.user,
            author_id=author.id
        )
        second_book.save()

        third_book = Book(
            title='Third book',
            genre='Mystery',
            cover_photo='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1284431932l/8253037.jpg',
            description='Cook Book Description',
            creator=self.user,
            author_id=author.id
        )
        third_book.save()

        self.client.force_login(self.user)

        response = self.client.get(reverse('details profile', kwargs={
            'pk': self.user.pk,
        }), follow=True)

        self.assertEqual(self.user.id, response.context['profile'].user_id)
        print(response.context['books_posted'])
        self.assertListEqual([third_book, second_book, book], list(response.context['books_posted']))
        self.assertListEqual([author], list(response.context['authors_created']))