from django.urls import path
from .views import dashboard, login, add_image, edit_image, IndexHome, thumb_image
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add-image/', add_image, name='add_image'),
    path('edit-image/<str:id>/', edit_image, name='edit_image'),
    path('thumb-image/<str:id>/<int:height>/<int:width>/', thumb_image, name='thumb_image'),
    path('', IndexHome.as_view(), name='index'),
]
