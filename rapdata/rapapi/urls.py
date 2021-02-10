from django.urls import include, path
from rest_framework import routers
from rapapi import views

router = routers.DefaultRouter()
router.register(r'artists', views.ArtistViewSet)

urlpatterns = [
    path('', include(router.urls))
]