from django.contrib.auth.models import User, Group

from data.models import Artist 


def create_user():
    user = User.objects.create(username='petrou', password="bahtiens")
    user_group = Group.objects.create(name='user')
    user_group.user_set.add(user)
    user_group.save()

    return user

def get_artist():
    return Artist.objects.all().first()