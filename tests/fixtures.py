import pytest


# ----------------------------------------------------------------
@pytest.fixture()
@pytest.mark.django_db
def test_auth_data(client, django_user_model) -> tuple:
    """
    A fixture to add user to database, login and return valid access token
    :param client:
    :param django_user_model:
    :return: tuple with user id and access token
    """
    email = 'test@example.ru'
    password = 'password123456'
    role = 'user'
    first_name = 'test_first_name'
    last_name = 'test_last_name'
    phone = '+79123456789'

    user = django_user_model.objects.create_user(
        email=email,
        password=password,
        role=role,
        first_name=first_name,
        last_name=last_name,
        phone=phone
    )

    response = client.post(
        '/api/token/',
        {
            'email': email,
            'password': password
        },
        format='json'
    )

    return response.data.get('access'), user
