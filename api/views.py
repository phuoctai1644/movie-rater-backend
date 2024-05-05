from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer, RatingByMovieSerializer
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny, )

    @action(detail=False, methods=['GET'])
    def profile(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs['pk'])

            if request.data is None:
                return Response({'message': 'Missing info!'}, status=status.HTTP_400_BAD_REQUEST)

            user.username = request.data['userName']
            user.email = request.data['email']
            user.first_name = request.data['firstName']
            user.last_name = request.data['lastName']
            user.save()
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            response = {'message': 'Cannot find this user!'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def change_password(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
            current_password = request.data['currentPassword']
            new_password = request.data['newPassword']
            if not user.check_password(raw_password=current_password):
                return Response({'message': 'Password not match!'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except:
            response = {'message': 'Cannot find this user!'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    authentication_classes = (TokenAuthentication, )
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            description = request.data['description']
            user = request.user

            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.description = description
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating updated', 'data': serializer.data}
            except:
                rating = Rating.objects.create(user=user, movie=movie, stars=stars, description=description)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating created', 'data': serializer.data}

            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'You need to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)

    def create(self, request, *args, **kwargs):
        response = {'message': 'You cant create rating with this API'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'You cant update rating with this API'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='by_movie/(?P<pk>\d+)')
    def by_movie_id(self, request, pk=None):
        ratings = Rating.objects.filter(movie__id=pk)
        serializer = RatingByMovieSerializer(ratings, many=True)
        return Response(serializer.data)
