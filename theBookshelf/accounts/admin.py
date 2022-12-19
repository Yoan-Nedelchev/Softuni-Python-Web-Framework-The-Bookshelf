from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model
from theBookshelf.accounts.forms.sign_up import SignUpForm

UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(auth_admin.UserAdmin):
    search_fields = ['username', 'email', ]
    ordering = ('username',)
    add_form = SignUpForm
    list_display = ['username', 'email', 'is_staff']
    readonly_fields = ('date_joined',)
    list_filter = ('is_staff',)
    fieldsets = (
        ('User Status', {'fields': ('is_superuser', 'is_staff',)}),
        ('Permission Groups', {'fields': ('groups',)}),
        ('Individual Permissions', {'fields': ('user_permissions',)}),
        ('User Information', {'fields': ('username', 'password', 'email')}),
    )
    add_fieldsets = (
        ('User Registration', {
            # 'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


