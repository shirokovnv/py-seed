"""
Testing API.
"""

from fastapi import status
from fastapi.testclient import TestClient

from api import app
from schema import req_schema

client = TestClient(app)


def test_read_seeds_ok():
    """
    Testing 200 response.
    """
    response = client.post(
        '/seeds',
        headers={'Content-type': 'application/json'},
        json={
            'count': 1,
            'format': 'json',
            'schema': req_schema
        })
    assert response.status_code == status.HTTP_200_OK


def test_read_seeds_unprocessable_entity():
    """
    Testing 422 response.
    """
    response = client.post(
        '/seeds',
        headers={'Content-type': 'application/json'},
        json={
            'count': 1,
            'format': 'json',
            'schema': {}
        })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
