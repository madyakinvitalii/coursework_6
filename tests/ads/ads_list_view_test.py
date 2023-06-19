import pytest
from ads.serializers import AdSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_list(client):
    ads = AdFactory.create_batch(4)
    expected_response = {
        'count': 4,
        'next': None,
        'previous': None,
        'results': AdSerializer(ads, many=True).data
    }
    response = client.get('/api/ads/')

    assert response.status_code == 200, 'Status code error'
    assert response.data is not None, 'HttpResponseError'
    assert response.data == expected_response, 'Wrong data expected'
