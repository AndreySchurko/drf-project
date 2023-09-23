from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from .utils import get_image_path, get_image_thumb_path
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import FileExtensionValidator
from .validators import validate_file_size
import uuid
from .managers import CustomUserManager
from django_advance_thumbnail import AdvanceThumbnailField
from django.urls import reverse


class ImageSize(models.Model):
    """
    Model for setting custom sizes for thumbnails
    """
    height = models.PositiveIntegerField(verbose_name='Image height, px',
                                         validators=[MinValueValidator(1), MaxValueValidator(10000)],
                                         help_text='Required')
    width = models.PositiveIntegerField(verbose_name='Image width, px', blank=True, default=1,
                                        validators=[MinValueValidator(1), MaxValueValidator(10000)])

    class Meta:
        ordering = ['height']

    def __str__(self):
        return f'{self.width}x{self.height}'


class Profile(models.Model):
    """
    Model for setting up account tiers
    """
    title = models.CharField(max_length=100, verbose_name='Account tier Title', blank=False)
    original_img_link = models.BooleanField(default=False, help_text='Link to originally uploaded image (Yes/No)')
    expires_img_link = models.BooleanField(default=False, help_text='Expiring link to the image (Yes/No)')
    img_size = models.ManyToManyField(ImageSize, related_name='image_size', blank=True,
                                      verbose_name='Available thumbnail sizes')

    class Meta:
        ordering = ['title']
        verbose_name = 'Account tier'
        verbose_name_plural = 'Account tiers'

    def __str__(self):
        return self.title


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='image_user')
    default_image = models.ImageField(upload_to=get_image_path,
                                      validators=[
                                          validate_file_size,
                                          FileExtensionValidator(allowed_extensions=settings.ALLOWED_IMAGE_EXTENSIONS)
                                      ],
                                      help_text='Only JPG/JPEG or PNG files. Max.size 20 Mb.')
    thumbnail = AdvanceThumbnailField(source_field='default_image', upload_to=get_image_thumb_path,
                                      null=True, blank=True, size=(100, 100))
    title = models.CharField(max_length=255, blank=False, verbose_name='Image title', help_text='Required')
    author = models.CharField(max_length=255, blank=True, verbose_name='Image author')
    expires = models.PositiveIntegerField(blank=True, null=True,
                                          validators=[MinValueValidator(300), MaxValueValidator(30000)],
                                          verbose_name='Link will expire, sec.',
                                          help_text='Min. 300, Max. 30 000 seconds')
    published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['published'])
        ]

    def __str__(self):
        return f'{self.id}'

    def get_absolute_url(self):
        return reverse('edit_image', kwargs={'id': self.pk})


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='user_profile', blank=True, null=True,
                                verbose_name='Account tier')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
