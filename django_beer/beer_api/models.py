from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Style(models.Model):
	style = models.CharField(max_length=100)
	description =  models.TextField(max_length=5000)

	def __unicode__(self):
		return self.style

class GlassType(models.Model):
	glass_type = models.CharField(max_length=100)
	description =  models.TextField(max_length=5000)

	def __unicode__(self):
		return self.glass_type

class Brewery(models.Model):
	added_by_user = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=200)
	brewery_location = models.CharField(max_length=1000)

	class Meta:
		verbose_name = 'Brewery'
		verbose_name_plural = 'Breweries'


	def __unicode__(self):
		return '%s - %s' % (self.name,self.brewery_location)

class Beer(models.Model):
	added_by_user = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=200)
	ibu = models.IntegerField(
			validators=[
				MaxValueValidator(100),
				MinValueValidator(0),
			]
		)
	calories = models.IntegerField(
			validators=[
				MinValueValidator(0),
			]
		)
	abv = models.DecimalField(
		max_digits=5,
		decimal_places=2,
		validators=[
				MaxValueValidator(100),
				MinValueValidator(0),
			])
	brewery = models.ForeignKey(Brewery)
	style = models.ForeignKey(Style)
	glass_type = models.ForeignKey(GlassType)
	description =  models.TextField(max_length=5000)


	def __unicode__(self):
		return self.name

class BeerReview(models.Model):
	user = models.ForeignKey(User)
	beer = models.ForeignKey(Beer)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	aroma = models.IntegerField(
			validators=[
				MaxValueValidator(5),
				MinValueValidator(1),
			]
		)
	appearance = models.IntegerField(
			validators=[
				MaxValueValidator(5),
				MinValueValidator(1),
			]
		)
	taste = models.IntegerField(
			validators=[
				MaxValueValidator(10),
				MinValueValidator(1),
			]
		)
	palate = models.IntegerField(
			validators=[
				MaxValueValidator(5),
				MinValueValidator(1),
			]
		)
	bottle_style = models.IntegerField(
			validators=[
				MaxValueValidator(5),
				MinValueValidator(1),
			]
		)
	comments =  models.TextField(max_length=5000)

	def __unicode__(self):
		return '%s - %s' % (self.id,self.beer)

class Favorite(models.Model):
	user = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	beer = models.ForeignKey(Beer)

	def __unicode__(self):
		return '%s - %s' % (self.user,self.beer)
