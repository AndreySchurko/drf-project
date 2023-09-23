from rest_framework import serializers
from api.models import CustomUser, ImageSize, Profile, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'profile']


class ImageSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageSize
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    user_id = PublicUserSerializer(read_only=True)

    class Meta:
        model = Image
        fields = ['id', 'default_image', 'title', 'author', 'created', 'updated', 'user_id']


class AuthImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'default_image', 'title', 'author', 'expires', 'published', 'created', 'updated', 'user_id']
        read_only_fields = ['id', 'user_id', 'created', 'updated']


class UpdateAuthImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'title', 'author', 'expires', 'published', 'created', 'updated', 'user_id']
        read_only_fields = ['id', 'user_id', 'created', 'updated']


class BasicAuthImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'default_image', 'title', 'author', 'published', 'created', 'updated', 'user_id']
        read_only_fields = ['id', 'user_id', 'created', 'updated']

class UpdateBasicAuthImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'title', 'author', 'published', 'created', 'updated', 'user_id']
        read_only_fields = ['id', 'user_id', 'created', 'updated']
