import factory

from ads.models import Ad, Comment
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    password = 'password123456'
    first_name = 'test_first_name'
    last_name = 'test_last_name'
    is_active = True
    phone = '+79123456789'


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    title = 'Test'
    description = 'Test'
    price = 50
    author = factory.SubFactory(UserFactory)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = 'test_comment'
    author = factory.SubFactory(UserFactory)
    ad = factory.SubFactory(AdFactory)
    created_at = None
