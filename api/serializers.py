from rest_framework import serializers
from .models import Movie, Rating
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(source='get_avatar')

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'avatar')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': True}
        }

    def get_avatar(self, obj):
        request = self.context.get('request')
        avatar = obj.avatar.url
        return request.build_absolute_uri(avatar)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'year', 'total_rating', 'avg_rating', 'thumbnail', 'type', 'trailer_url')


class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    movie = MovieSerializer(many=False)

    class Meta:
        model = Rating
        fields = ('id', 'stars', 'description', 'user', 'movie', 'created_at', 'modified_at')


class RatingByMovieSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Rating
        fields = ('id', 'stars', 'description', 'user', 'created_at', 'modified_at')
