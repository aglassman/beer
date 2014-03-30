from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import *

user_fields = (
			'url',
        	'id', 
        	'username')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = user_fields

class AdminUserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = (
			'url',
			'id',
			'username',
			'email',
			'password',
			'is_staff',
			'is_active',)

class StyleSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Style
		fields = (
			'url',
			'id',
			'style',
			'description')

class GlassTypeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = GlassType
		fields = (
			'url',
			'id',
			'glass_type',
			'description')

class BrewerySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Brewery
		fields = (
			'url',
			'id',
			'name',
			'brewery_location')

beer_fields = (
			'url',
			'id',
			'created_at',
			'added_by_user',
			'name',
			'ibu',
			'calories',
			'abv',
			'brewery',
			'style',
			'glass_type',
			'description')

class BeerSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Beer
		fields = beer_fields

class DeepBeerSerializer(serializers.HyperlinkedModelSerializer):
	brewery = BrewerySerializer()
	style = StyleSerializer()
	glass_type = GlassTypeSerializer()
	added_by_user = UserSerializer()
	class Meta:
		model = Beer
		fields = beer_fields
		depth=1

beer_review_fields = (
			'url',
			'id',
			'user',
			'beer',
			'aroma',
			'appearance',
			'taste',
			'palate',
			'bottle_style',
			'comments')

class BeerReviewSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = BeerReview
		fields = beer_review_fields

class DeepBeerReviewSerializer(serializers.HyperlinkedModelSerializer):
	user = UserSerializer()
	beer = BeerSerializer()

	class Meta:
		model = BeerReview
		fields = beer_review_fields
		depth=1

favorite_fields = (
			'url',
			'id',
			'user',
			'beer',)

class FavoriteSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Favorite
		fields = favorite_fields

class DeepFavoriteSerializer(serializers.HyperlinkedModelSerializer):
	user = UserSerializer()
	beer = BeerSerializer()
	
	class Meta:
		model = Favorite
		fields = favorite_fields
		depth=1