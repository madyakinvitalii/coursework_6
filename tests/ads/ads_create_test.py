import pytest


@pytest.mark.django_db
def test_create_ad(client, test_auth_data: tuple) -> None:
    """
    Function to create test advertisement and compare response with test data
    :param client: test client
    :param test_auth_data: tuple(auth_token, auth_id)
    """
    auth_token: str = test_auth_data[0]
    user = test_auth_data[1]

    advertisement: dict = {
        "title": 'Test_ad',
        "description": 'Test_description',
        "price": 50,
        "phone": user.phone,
        "author_id": user.pk,
        "author_first_name": user.first_name,
        "author_last_name": user.last_name,
    }

    response = client.post(
        '/api/ads/',
        data=advertisement,
        content_type='application/json',
        HTTP_AUTHORIZATION='Bearer ' + auth_token
    )

    expected_response: dict = {
        "pk": 1,
        "title": 'Test_ad',
        "description": 'Test_description',
        "price": 50,
        "phone": user.phone,
        "author_id": response.data.get('pk'),
        "author_first_name": user.first_name,
        "author_last_name": user.last_name,
        "image": None
    }

    assert response.status_code == 201, 'Status code error'
    assert response.data is not None, 'HttpResponseError'
    assert response.data == expected_response, 'Wrong data expected'


@pytest.mark.django_db
def test_create_ad_401(client, test_auth_data: tuple) -> None:
    """
    Function to create test advertisement without token
    :param client: test client
    :param test_auth_data: tuple(auth_token, auth_id)
    """
    user = test_auth_data[1]

    advertisement: dict = {
        "title": 'Test_ad',
        "description": 'Test_description',
        "price": 50,
        "phone": user.phone,
        "author_id": user.pk,
        "author_first_name": user.first_name,
        "author_last_name": user.last_name,
    }

    response = client.post(
        '/api/ads/',
        data=advertisement,
        content_type='application/json',
    )

    expected_response: dict = {
        'detail': 'Учетные данные не были предоставлены.'
    }

    assert response.status_code == 401, 'Status code error'
    assert response.data is not None, 'HttpResponseError'
    assert response.data == expected_response, 'Wrong data expected'
