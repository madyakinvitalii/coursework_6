import pytest


@pytest.mark.django_db
def test_create_comment(client, ad, test_auth_data: tuple) -> None:
    """
    Function to create test comment and compare response with test data
    :param client: test client
    :param test_auth_data: tuple(auth_token, auth_id)
    """
    auth_token: str = test_auth_data[0]
    user = test_auth_data[1]

    comment: dict = {
        "text": 'Test',
    }

    response = client.post(
        f'/api/ads/{ad.pk}/comments/',
        data=comment,
        content_type='application/json',
        HTTP_AUTHORIZATION='Bearer ' + auth_token
    )

    expected_response: dict = {
        "pk": 1,
        "text": 'Test',
        "ad_id": ad.pk,
        "author_id": user.pk,
        "author_first_name": user.first_name,
        "author_last_name": user.last_name,
        "author_image": None,
        "created_at": None
    }
    response.data['created_at'] = None

    assert response.status_code == 201, 'Status code error'
    assert response.data is not None, 'HttpResponseError'
    assert response.data == expected_response, 'Wrong data expected'


@pytest.mark.django_db
def test_create_comment_401(client, test_auth_data: tuple) -> None:
    """
    Function to create test comment without token
    :param client: test client
    :param test_auth_data: tuple(auth_token, auth_id)
    """

    comment: dict = {
        "text": 'Test',
    }

    response = client.post(
        '/api/ads/',
        data=comment,
        content_type='application/json',
    )

    expected_response: dict = {
        'detail': 'Учетные данные не были предоставлены.'
    }

    assert response.status_code == 401, 'Status code error'
    assert response.data is not None, 'HttpResponseError'
    assert response.data == expected_response, 'Wrong data expected'
