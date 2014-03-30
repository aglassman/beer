from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import decorators
from rest_framework import status
from rest_framework.response import Response
from beer_api.serializers import *
from models import *
import datetime


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @decorators.link()
    def favorites(self,request,pk=None):
        user = User.objects.filter(id=pk)
        favorites = Favorite.objects.filter(user=user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)


class StyleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Style.objects.all()
    serializer_class = StyleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class GlassTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = GlassType.objects.all()
    serializer_class = GlassTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BreweryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Brewery.objects.all()
    serializer_class = BrewerySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BeerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self,request):
        max_beers_per_day=1
        user = request.user
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        beers_added_today = Beer.objects.filter(created_at__gte=yesterday)
        if len(beers_added_today) >= max_beers_per_day:
            content = {'detail':'You added the maximum amout of beers for today, try again tomorrow'}
            return Response(content,status=status.HTTP_403_FORBIDDEN)
        else:
            return super(BeerViewSet,self).create(request)

    @decorators.link()
    def deep(self,request,pk=None):
        beer = Beer.objects.filter(id=pk)
        serializer = DeepBeerSerializer(beer)
        return Response(serializer.data)

class BeerReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = BeerReview.objects.all()
    serializer_class = BeerReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @decorators.link()
    def deep(self,request,pk=None):
        beer_review = BeerReview.objects.filter(id=pk)
        serializer = DeepBeerReviewSerializer(beer_review)
        return Response(serializer.data)

class FavoriteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @decorators.link()
    def deep(self,request,pk=None):
        favorite = Favorite.objects.filter(id=pk)
        serializer = DeepFavoriteSerializer(favorite)
        return Response(serializer.data)

@decorators.api_view(('GET',))
def beer_reviews(request,id):
    """
    List all reviews for a particular beer.
    """

    if request.method == 'GET':
        beer = Beer.objects.filter(id=id)
        beerReviews = BeerReview.objects.filter(beer=beer)
        serializer = BeerReviewSerializer(beerReviews, many=True)
        return Response(serializer.data)
