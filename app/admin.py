from django.contrib import admin
from . models import Follow , Post , Like , Comment 
from django.contrib.auth import get_user_model
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

# Register your models here.
User = get_user_model()
@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )


admin.site.register(Follow)



class LikeInline(admin.TabularInline):
    model = Like

class CommentInline(admin.TabularInline):
    model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [
        LikeInline,
        CommentInline
    ]