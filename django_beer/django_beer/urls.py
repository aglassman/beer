from django.conf.urls import patterns, url, include
from rest_framework import routers
from beer_api import views
from django.contrib import admin

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'styles', views.StyleViewSet)
router.register(r'glass_types', views.GlassTypeViewSet)
router.register(r'breweries', views.BreweryViewSet)
router.register(r'beers', views.BeerViewSet)
router.register(r'beer_reviews', views.BeerReviewViewSet)
router.register(r'favorites', views.FavoriteViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
	url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^beer/(?P<id>\d+)/reviews/$',views.beer_reviews),

)
