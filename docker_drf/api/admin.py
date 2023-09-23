from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, ImageSize, Profile, Image


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'is_superuser', 'profile',)
    list_filter = ('is_staff', 'is_active', 'profile',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('profile', 'first_name', 'last_name', 'is_staff', 'is_active',
                                    'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'profile', 'first_name', 'last_name', 'password1', 'password2', 'is_staff',
                'is_active', 'groups', 'user_permissions'
            )}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(ImageSize)
class ImageSizeAdmin(admin.ModelAdmin):
    list_display = ['height', 'width']
    list_display_links = ['height', 'width']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['title', 'original_img_link', 'expires_img_link']
    list_filter = ['original_img_link', 'expires_img_link']
    list_editable = ['original_img_link', 'expires_img_link']
    list_display_links = ['title']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    def get_image(self, obj):
        if obj.thumbnail:
            return mark_safe(f'<img src="{obj.thumbnail.url}" height="50" width="auto">')
        return '-'

    get_image.short_description = "IMG THUMB"
    list_display = ['id', 'user_id', 'get_image', 'published', 'active', 'created', 'updated']
    raw_id_fields = ['user_id']
    list_filter = ['published', 'active']
    #readonly_fields = ['user_id', 'created', 'updated', 'default_image', 'expires', 'published']
    fields = ['user_id', 'default_image', 'expires', 'title', 'author', 'published', 'active']
    list_editable = ['active']
    save_on_top = True
    list_display_links = ['id']
