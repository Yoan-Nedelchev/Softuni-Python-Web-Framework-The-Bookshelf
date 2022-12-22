from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views, login, get_user_model
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.generic import DetailView, UpdateView, DeleteView
from theBookshelf.accounts.forms.edit_profile import EditProfileForm
from theBookshelf.accounts.forms.login import LoginForm
from theBookshelf.accounts.forms.sign_up import SignUpForm
from theBookshelf.accounts.models import Profile
from theBookshelf.author.models import Author
from theBookshelf.book.models import Book

UserModel = get_user_model()


class SignUpView(views.CreateView):
    template_name = 'accounts/sign-up.html'
    form_class = SignUpForm

    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)
        return result


class SignInView(auth_views.LoginView):
    template_name = 'accounts/sign-in.html'
    authentication_form = LoginForm


class SignOutView(auth_views.LogoutView):
    template_name = 'accounts/sign-out.html'


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = context['profile']

        app_user = UserModel.objects.get(pk=profile.user_id)
        is_owner = profile.pk == self.request.user.pk
        books_posted = Book.objects.filter(creator_id=profile.user_id)
        authors_created = Author.objects.filter(creator_id=profile.user_id)

        context['is_owner'] = is_owner
        context['books_posted'] = books_posted
        context['authors_created'] = authors_created
        context['username'] = app_user.username

        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'accounts/edit_profile.html'
    form_class = EditProfileForm

    def get_success_url(self):
        return reverse_lazy('details profile', kwargs={'pk': self.kwargs.get('pk')})


class DeleteAccountView(LoginRequiredMixin, DeleteView):
    template_name = 'accounts/delete_account.html'
    model = UserModel
    success_url = reverse_lazy('index')
