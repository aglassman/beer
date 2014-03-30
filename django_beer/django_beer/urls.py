from django.conf.urls import patterns, url, include
from rest_framework import routers
from beer_api import views
from django.contrib import admin

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'user_admin', views.AdminUserViewSet,base_name='user_admin')
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
    url(r'^user_list/favorites/(?P<pk>[0-9]+)/$', views.UserFavoriteListView.as_view()),
    url(r'^user_list/beer_contributions/(?P<pk>[0-9]+)/$', views.UserBeerListView.as_view()),
    url(r'^user_list/beer_reviews/(?P<pk>[0-9]+)/$', views.UserBeerReviewListView.as_view()),
    url(r'^beer_list/reviews/(?P<pk>[0-9]+)/$', views.BeerReviewListView.as_view()),
    url(r'^beer_list/overall/(?P<pk>[0-9]+)/$', views.BeerReviewCalculated.as_view()),
    url(r'^beer_list/favorited/(?P<pk>[0-9]+)/$', views.BeerFavoritesListView.as_view()),

)
