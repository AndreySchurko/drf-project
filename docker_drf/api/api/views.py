from api.api.filters import IsUserFilterBackend
from api.api.permissions import IsCurrentUser
from api.api.serializers import *
from api.models import CustomUser, ImageSize, Profile, Image
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from easy_thumbnails.files import get_thumbnailer
from django.conf import settings
from django.utils.timezone import now
from rest_framework.exceptions import APIException


class UserViewSet(viewsets.ModelViewSet):
    """
    GET, POST, DEL, PUT Users
    Available only for administrator
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class ImageSizeViewSet(viewsets.ModelViewSet):
    """
    GET, POST, DEL, PUT Image Sizes
    Available only for administrator
    """
    queryset = ImageSize.objects.all()
    serializer_class = ImageSizeSerializer
    permission_classes = [IsAdminUser]


class ProfileViewSet(viewsets.ModelViewSet):
    """
    GET, POST, DEL, PUT Account Tiers
    Available only for administrator
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]


@api_view(['GET'])
def published_images(request):
    """
    List of published images
    Available to everyone
    """
    images = Image.objects.filter(published=True, active=True).select_related('user_id')
    serializer = ImageSerializer(images, many=True)
    return Response(serializer.data)


class ImageList(viewsets.ModelViewSet):
    """
    List of images added by an authorized user
    """
    queryset = Image.objects.filter(active=True)
    permission_classes = [IsAuthenticated, IsCurrentUser]
    filter_backends = (IsUserFilterBackend,)
    filterset_fields = ("user_id",)

    def get_serializer_class(self):
        if self.request.user.profile.expires_img_link == True:
            serializer_map = {
                'list': AuthImageSerializer,
                'create': AuthImageSerializer,
                'retrieve': AuthImageSerializer,
                'update': UpdateAuthImageSerializer
            }
            return serializer_map.get(self.action, AuthImageSerializer)
        else:
            serializer_map = {
                'list': BasicAuthImageSerializer,
                'create': BasicAuthImageSerializer,
                'retrieve': BasicAuthImageSerializer,
                'update': UpdateBasicAuthImageSerializer
            }
            return serializer_map.get(self.action, BasicAuthImageSerializer)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            serializer.save(user_id=user)
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_links(request, id=None):
    """
    Generate Links to thumbnail images
    """
    image = Image.objects.get(id=id)
    if image.expires:
        current_time = now()
        delta = current_time - image.created
        delta_sec = int(delta.total_seconds())
        if delta_sec >= image.expires:
            raise APIException('Sorry! The link has expired!', status_code=status.HTTP_403_FORBIDDEN)

        current_user = CustomUser.objects.get(id=request.user.pk)
        sizes = current_user.profile.img_size.all()
        thumbnailer = get_thumbnailer(f'{settings.BASE_DIR}/{image.default_image.url}')
        thumbnail_options = {'crop': True}
        thumb_url_list = []
        protocol = request.META['wsgi.url_scheme']
        domain = request.META['HTTP_HOST']
        full_path = protocol + "://" + domain
        for size in sizes:
            thumbnail_options.update({'size': (size.width, size.height)})
            thumb = thumbnailer.get_thumbnail(thumbnail_options)
            thumb_url_key = f'Thumb image {size.width}x{size.height}'
            thumb_url = {thumb_url_key: f'{full_path}{thumb.url}'}
            thumb_url_list.append(thumb_url)
        if current_user.profile.original_img_link:
            thumb_url_list.append({'Originally uploaded image': f'{full_path}{image.default_image.url}'})
    return Response(thumb_url_list)
