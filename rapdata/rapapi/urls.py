from django.urls import include, path
from rest_framework import routers

from rest_framework_swagger.views import get_swagger_view
from rapapi import views

router = routers.DefaultRouter()
schema_view = get_swagger_view(title='RAPDATA API')

router.register(r'artists', views.ArtistViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('docs', schema_view)
]