from django.contrib.auth.models import User, Group

from data.models import Artist 


def create_user():
    user, created = User.objects.get_or_create(username='petrou', password="bahtiens")
    if created:
        user_group = Group.objects.create(name='user')
        user_group.user_set.add(user)
        user_group.save()

    return user

def get_artist():
    return Artist.objects.all().first()

def get_user_from_username(username):
    return User.objects.get(username=username)