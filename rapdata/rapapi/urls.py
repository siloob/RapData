from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views as rest_views
from rest_framework_swagger.views import get_swagger_view
from rapapi.routers import CustomReadOnlyRouter

from rapapi import views

router = CustomReadOnlyRouter()
router.register(r'artists', views.ArtistViewSet)

schema_view = get_swagger_view(title='RAPDATA API')

urlpatterns = [
    path('', include(router.urls)),
    path('docs', schema_view),
    path('token/', rest_views.obtain_auth_token),
    path('user/', views.UserCreateView.as_view())
]