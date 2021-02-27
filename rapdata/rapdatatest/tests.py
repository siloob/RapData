from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from rapapi.views import ArtistViewSet
from rapapi.models import Artist

from rapdatatest.testutils.utils import create_user, get_artist

# Create your tests here.

class ArtistViewSetTest(TestCase):
    fixtures = ['artist.json']

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = create_user()
        
    def test_get_all_unauth(self):
        request = self.factory.get('/api/artists')
        response = ArtistViewSet.as_view({'get': 'list'})(request)
        
        self.assertEqual(response.status_code, 401)

    def test_get_all_auth_as_user(self):
        request = self.factory.get('/api/artists')
        force_authenticate(request, user=self.user)
        response = ArtistViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, 200)

    def test_get_artist_by_id(self):
        artist = get_artist()
        request = self.factory.get('/api/artists/%i' % artist.pk)
        force_authenticate(request, user=self.user)
        response = ArtistViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.data['results'][0]['name'], 'Kool Shen')
        self.assertEqual(response.data['results'][0]['id_music_story'], 5094)
        self.assertEqual(response.data['results'][0]['id_rap_genius'], 12547)
        self.assertEqual(response.data['results'][0]['genius_followers'], 28)

