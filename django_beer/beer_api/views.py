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
import logging
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import filters
from rest_framework import generics
from rest_framework.views import APIView

logger = logging.getLogger('beer')

def deepTest(request):
    return request.GET.get('deep', None) == 'y'

class AdminUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [custom_permissions.IsAdminOrReadOnly]
    filter_backends = (filters.OrderingFilter,)
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
    filter_backends = (filters.OrderingFilter,)

class StyleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Style.objects.all()
    serializer_class = StyleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (filters.OrderingFilter,)

class GlassTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = GlassType.objects.all()
    serializer_class = GlassTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (filters.OrderingFilter,)

class BreweryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Brewery.objects.all()
    serializer_class = BrewerySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (filters.OrderingFilter,)

class BeerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (filters.OrderingFilter,)

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

    def retrieve(self,request,pk=None):
        deep =  deepTest(request)
        try:
            beer = Beer.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = None
        if deep:
            serializer = DeepBeerSerializer(beer)
        else:
            serializer = BeerSerializer(beer)
        return Response(serializer.data)

class BeerReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = BeerReview.objects.all()
    serializer_class = BeerReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (filters.OrderingFilter,)

    def retrieve(self,request,pk=None):
        deep = deepTest(request)
        
        try:
            beer_review = BeerReview.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = None
        if deep:
            serializer = DeepBeerReviewSerializer(beer_review)
        else:
            serializer = BeerReviewSerializer(beer_review)
        return Response(serializer.data)

    def create(self,request):
        serializer = BeerReviewSerializer(data=request.DATA)
        
        try:
            beer = Beer.objects.get(id=request.DATA['beer'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user
        last_week = datetime.date.today() - datetime.timedelta(days=7)
        results = BeerReview.objects.filter(
                user=user
            ).filter(
                beer=beer
            ).filter(
                created_at__gte=last_week
            )
        reviewed_in_past_week = len(results) >= 1

        if reviewed_in_past_week:
            content = {'detail':'You have already reviewed this beer within the past week. Try again later.'}
            return Response(content,status=status.HTTP_403_FORBIDDEN)
        else:
            if serializer.is_valid():
                serializer.save()
                beerReview = BeerReview.objects.get(pk=serializer.data['id'])
                beerReview.user = user
                beerReview.save()
                outserializer = BeerReviewSerializer(beerReview)
                return Response(outserializer.data,status=status.HTTP_201_CREATED)
            content = {'detail':'Failed to create beer review.'}
            return Response(content,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FavoriteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (filters.OrderingFilter,)

    def retrieve(self,request,pk=None):
        deep = deepTest(request)
        favorite = None
        try:
            favorite = Favorite.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = None
        if deep:
            serializer = DeepFavoriteSerializer(favorite)
        else:
            serializer = FavoriteSerializer(favorite)
        return Response(serializer.data)

    def create(self,request):
        user = request.user
        try:   
            beer = Beer.objects.get(id=request.DATA['beer'])
        except ObjectDoesNotExist:
            content = {'detail':'You specified a beer that could not be found.'}
            return Response(content,status=status.HTTP_404_NOT_FOUND)

        favorite_beer = Favorite.objects.filter(
                user=user
            ).filter(
                beer = beer
            )

        if len(favorite_beer) > 0:
            content = {'detail':'You have already favorited this beer.'}
            return Response(content,status=status.HTTP_403_FORBIDDEN)

        serializer = FavoriteSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            favorite = Favorite.objects.get(pk=serializer.data['id'])
            favorite.user = user
            favorite.save()
            outserializer = FavoriteSerializer(favorite)
            return Response(outserializer.data,status=status.HTTP_201_CREATED)
        content = {'detail':'Failed to create favorite.'}
        return Response(content,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserFavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    filter_backends = (filters.OrderingFilter,)
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        try:
            user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            user=None

        favorites = Favorite.objects.filter(user=user)
        
        return favorites

class UserBeerListView(generics.ListAPIView):
    serializer_class = BeerSerializer
    filter_backends = (filters.OrderingFilter,)
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        try:
            user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            user=None

        beers = Beer.objects.filter(added_by_user=user)
        
        return beers

class UserBeerReviewListView(generics.ListAPIView):
    serializer_class = BeerReviewSerializer
    filter_backends = (filters.OrderingFilter,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        try:
            user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            user=None

        beerReviews = BeerReview.objects.filter(user=user)
        
        return beerReviews


class BeerFavoritesListView(generics.ListAPIView):
    """
    Returns list of users who have favorited this beer.
    """

    serializer_class = UserSerializer
    filter_backends = (filters.OrderingFilter,)
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        try:
            beer = Beer.objects.get(id=pk)
        except ObjectDoesNotExist:
            beer=None

        favorites = Favorite.objects.filter(beer=beer)
        users = []
        for favorite in favorites:
            users.append(favorite.user)
        return users


class BeerReviewListView(generics.ListAPIView):
    """
    List all reviews for a particular beer.
    """

    serializer_class = BeerReviewSerializer
    filter_backends = (filters.OrderingFilter,)

    def get_queryset(self):
        pk = self.kwargs['pk']

        try:
            beer = Beer.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        beerReviews = BeerReview.objects.filter(beer=beer)
        return beerReviews


class BeerReviewCalculated(APIView):
    """
    Average all reviews for a particular beer.
    """

    serializer_class = BeerReviewSerializer
    
    def get(self, request, format=None,pk=None):
        deep = deepTest(request)
        
        try:
            beer = Beer.objects.get(id=pk)
        except ObjectDoesNotExist:
            content = {'detail':'You specified a beer that could not be found.'}
            return Response(content,status=status.HTTP_404_NOT_FOUND)


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

        serializer = None
        if deep:
            serializer = DeepBeerReviewSerializer(averageReview)
        else:
            serializer = BeerReviewSerializer(averageReview)
        return Response(serializer.data)