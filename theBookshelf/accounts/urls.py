from django.urls import path, include


from theBookshelf.accounts.views import SignUpView, SignInView, SignOutView, ProfileDetailsView, EditProfileView, \
    DeleteAccountView

urlpatterns = (
    path('register/', SignUpView.as_view(), name='sign up'),
    path('login/', SignInView.as_view(), name='sign in'),
    path('sign-out/', SignOutView.as_view(), name='sign out'),
    path('profile/<int:pk>', include([
        path('', ProfileDetailsView.as_view(), name='details profile'),
        path('edit/', EditProfileView.as_view(), name='edit profile'),
        path('delete/', DeleteAccountView.as_view(), name='delete account'),
    ]))
)


