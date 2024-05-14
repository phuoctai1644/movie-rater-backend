from rest_framework import serializers
from .models import Movie, Rating, User
from rest_framework.authtoken.models import Token
import json


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class MovieSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(source='get_type')

    def get_type(self, obj):
        return json.loads(obj.type)

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
