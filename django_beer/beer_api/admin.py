from django.contrib import admin
from beer_api.models import *

class StyleAdmin(admin.ModelAdmin):
	list_display = ('style',)

class GlassTypeAdmin(admin.ModelAdmin):
	list_display = ('glass_type',)

class BreweryAdmin(admin.ModelAdmin):
	list_display = ('name',)

class BeerAdmin(admin.ModelAdmin):
	list_display = ('name','brewery')

class BeerReviewAdmin(admin.ModelAdmin):
	list_display = ('user','beer')

class FavoriteAdmin(admin.ModelAdmin):
	list_display = ('user','beer')

admin.site.register(Style,StyleAdmin)
admin.site.register(GlassType,GlassTypeAdmin)
admin.site.register(Brewery,BreweryAdmin)
admin.site.register(Beer,BeerAdmin)
admin.site.register(BeerReview,BeerReviewAdmin)
admin.site.register(Favorite,FavoriteAdmin)
