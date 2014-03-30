from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import *

user_fields = (
        	'id', 
        	'username')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = user_fields

class AdminUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'id',
			'username',
			'email',
			'password',
			'is_staff',
			'is_active',)

class StyleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Style
		fields = (
			'id',
			'style',
			'description')

class GlassTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = GlassType
		fields = (
			'id',
			'glass_type',
			'description')

class BrewerySerializer(serializers.ModelSerializer):
	class Meta:
		model = Brewery
		fields = (
			'id',
			'name',
			'brewery_location')

beer_fields = (
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

class BeerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Beer
		fields = beer_fields

class DeepBeerSerializer(serializers.ModelSerializer):
	brewery = BrewerySerializer()
	style = StyleSerializer()
	glass_type = GlassTypeSerializer()
	added_by_user = UserSerializer()
	class Meta:
		model = Beer
		fields = beer_fields
		depth=1

beer_review_fields = (
			'id',
			'created_at',
			'user',
			'beer',
			'aroma',
			'appearance',
			'taste',
			'palate',
			'bottle_style',
			'comments')

class BeerReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = BeerReview
		fields = beer_review_fields

class DeepBeerReviewSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	beer = BeerSerializer()

	class Meta:
		model = BeerReview
		fields = beer_review_fields
		depth=1

favorite_fields = (
			'id',
			'user',
			'beer',)

class FavoriteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Favorite
		fields = favorite_fields

class DeepFavoriteSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	beer = BeerSerializer()
	
	class Meta:
		model = Favorite
		fields = favorite_fields
		depth=1