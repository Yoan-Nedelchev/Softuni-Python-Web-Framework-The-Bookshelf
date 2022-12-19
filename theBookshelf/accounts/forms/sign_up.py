from django.contrib.auth import forms as auth_forms, get_user_model

UserModel = get_user_model()


class SignUpForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD, 'email', 'password1', 'password2')

    # save with data for profile
    def save(self, commit=True):
        user = super().save(commit=commit)
        return user
