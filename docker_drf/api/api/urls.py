from django.urls import include, path
from rest_framework import routers
from api.api.views import UserViewSet, ImageSizeViewSet, ProfileViewSet, published_images, ImageList, get_links

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'image-sizes', ImageSizeViewSet)
router.register(r'account-tiers', ProfileViewSet)
router.register(r'image-list', ImageList)


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),  # Authenticated URLs
    path('published-images/', published_images, name='published_images'),  # List of published images
    path('get-links/<str:id>/', get_links, name='get_links'),  # Links to thumbnail images
    path('', include(router.urls)),  # Home API Page
]
