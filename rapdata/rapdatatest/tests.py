from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from rapapi.views import ArtistViewSet, UserCreateView, GetRequestLimit

from rapdatatest.testutils.utils import create_user, get_artist, get_user_from_username


# Create your tests here.

class ArtistViewSetTest(TestCase):
    fixtures = ['artist.json']

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = create_user()
        self.artist = get_artist()
        self.view = ArtistViewSet.as_view({'get': 'list'})

    def test_get_all_unauth(self):
        request = self.factory.get('/api/artists')
        response = self.view(request)

        self.assertEqual(response.status_code, 401)

    def test_get_all_auth_as_user(self):
        request = self.factory.get('/api/artists')
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, 200)

    def test_get_artist_by_id(self):
        request = self.factory.get('/api/artists/%i' % self.artist.pk)
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['results'][0]['name'], self.artist.name)
        self.assertEqual(response.data['results'][0]['id_music_story'], self.artist.id_music_story)
        self.assertEqual(response.data['results'][0]['id_rap_genius'], self.artist.id_rap_genius)
        self.assertEqual(response.data['results'][0]['genius_followers'], self.artist.genius_followers)


class UserCreateTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = create_user()
        self.view = UserCreateView.as_view()
        self.data = {
            'username': 'anka',
            'password': 'bahtiens'
        }

    def test_create_user_from_user(self):
        request = self.factory.post('/api/user/', self.data)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 403)

    def test_create_user_from_admin(self):
        self.user.is_staff = True
        self.user.save()

        request = self.factory.post('/api/user/', self.data)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        response.render()

        user_created = get_user_from_username(self.data['username'])

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data['token'])
        self.assertEqual(user_created.username, self.data['username'])
        self.assertEqual(user_created.password, self.data['password'])


class GetLimitsRequestsTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = create_user()
        self.view = GetRequestLimit.as_view()

    def test_get_limits_unauth(self):
        request = self.factory.get('/api/requests')
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 401)

    def test_get_limits_auth(self):
        request = self.factory.get('/api/requests')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 200)
