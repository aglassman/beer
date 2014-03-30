from django.contrib.auth.models import User
from rest_framework import permissions
from beer_api import permissions as custom_permissions
from rest_framework import viewsets
from rest_framework import decorators
from rest_framework import status
from rest_framework.response import Response
from beer_api.serializers import *
from models import *
import datetime

class AdminUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [custom_permissions.IsAdminOrReadOnly]

    def create(self,request):
        serializer = AdminUserSerializer(data=request.DATA)
        if serializer.is_valid():
            new_user = User.objects.create_user(
                serializer.data['username'],
                serializer.data['email'],
                serializer.data['password'])
            new_user.is_staff = serializer.data['is_staff']
            new_user.is_active = serializer.data['is_active']
            new_user.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            content = {'detail':'User creation failed.'}
            return Response(content,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @decorators.link()
    def favorites(self,request,pk=None):
        user = User.objects.filter(id=pk)
        favorites = Favorite.objects.filter(user=user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    @decorators.link()
    def beer_contributions(self,request,pk=None):
        user = User.objects.filter(id=pk)
        beers = Beer.objects.filter(added_by_user=user)
        serializer = BeerSerializer(beers, many=True)
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
        beers_added_today = Beer.objects.filter(
                added_by_user=user
            ).filter(
                created_at__gte=yesterday
            )
        if len(beers_added_today) >= max_beers_per_day:
            content = {'detail':'You added the maximum amout of beers for today, try again tomorrow'}
            return Response(content,status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = BeerSerializer(data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                beer = Beer.objects.get(pk=serializer.data['id'])
                beer.added_by_user = user
                beer.save()
                outserializer = BeerSerializer(beer)
                return Response(outserializer.data,status=status.HTTP_201_CREATED)
            content = {'detail':'Failed to create beer.'}
            return Response(content,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @decorators.link()
    def deep(self,request,pk=None):
        beer = Beer.objects.filter(id=pk)
        serializer = DeepBeerSerializer(beer)
        return Response(serializer.data)

    @decorators.link()
    def reviews(self,request,pk=None):
        """
        List all reviews for a particular beer.
        """

        if request.method == 'GET':
            beer = Beer.objects.filter(id=pk)
            beerReviews = BeerReview.objects.filter(beer=beer)
            serializer = BeerReviewSerializer(beerReviews, many=True)
            return Response(serializer.data)

    @decorators.link()
    def overall(self,request,pk=None):
        """
        List all reviews for a particular beer.
        """

        if request.method == 'GET':
            beer = Beer.objects.get(pk=pk)
            beerReviews = BeerReview.objects.filter(beer=beer)
            aroma = 0
            appearance = 0
            taste = 0
            palate = 0
            bottle_style = 0
            num_reviews = len(beerReviews)
            
            for beerReview in beerReviews:
                aroma += beerReview.aroma
                appearance += beerReview.appearance
                taste += beerReview.taste
                palate += beerReview.palate
                bottle_style += beerReview.bottle_style


            averageReview = BeerReview()
            averageReview.beer = beer
            averageReview.aroma = int(round(aroma/num_reviews))
            averageReview.appearance = int(round(appearance/num_reviews))
            averageReview.taste = int(round(taste/num_reviews))
            averageReview.palate =int(round(palate/num_reviews))
            averageReview.bottle_style = int(round(bottle_style/num_reviews))
            averageReview.comments = 'Results based on %s reviews' % (num_reviews)
            serializer = BeerReviewSerializer(averageReview)
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
