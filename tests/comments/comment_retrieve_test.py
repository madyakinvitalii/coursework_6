import pytest


@pytest.mark.django_db
def test_retrieve_comment(client, ad, comment, test_auth_data):
    auth_token = test_auth_data[0]
    user = test_auth_data[1]

    response = client.get(
        f'/api/ads/{ad.pk}/comments/{comment.pk}/',
        HTTP_AUTHORIZATION='Bearer ' + auth_token
    )

    expected_response: dict = {
        "pk": comment.pk,
        "text": 'test_comment',
        "ad_id": ad.pk,
        "author_id": 18,
        "author_first_name": 'test_first_name',
        "author_last_name": user.last_name,
        "author_image": None,
        "created_at": None
    }

    response.data['created_at'] = None
    assert response.status_code == 200, 'Status code error'
    assert response.data is not None, 'HttpResponseError'
    assert response.data == expected_response, 'Wrong data expected'


@pytest.mark.django_db
def test_retrieve_comment_401(client, comment, ad, test_auth_data):
    response = client.get(
        f'/api/ads/{ad.pk}/comments/{comment.pk}/',
    )

    expected_response: dict = {
        'detail': 'Учетные данные не были предоставлены.'
    }

    assert response.status_code == 401, 'Status code error'
    assert response.data is not None, 'HttpResponseError'
    assert response.data == expected_response, 'Wrong data expected'
