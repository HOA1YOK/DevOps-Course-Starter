import os

import pytest
import requests
from dotenv import find_dotenv, load_dotenv

from todo_app import app


@pytest.fixture
def client():
    # use our test integration .env.test config instead of the 'real' .env
    file_path = find_dotenv(".env.test")
    load_dotenv(file_path, override=True)

    # create the new app
    test_app = app.create_app()

    # flask apps have an in-built 'test_client' module
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client  # yield keyword is basically the 'return' for generators


class StubResponse:
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    # This mocks the response.json call from the requests response
    def json(self):
        return self.fake_response_data


def stub(url, headers, params={}, verify=False):
    test_board_id = os.environ.get("BOARD_ID")

    if url == f"https://api.trello.com/1/boards/{test_board_id}/lists":
        # for each url request, we build a fake response
        fake_response_data = [
            {"id": "456def", "name": "To Do", "idBoard": "1234567890abc"},
            {
                "id": "456abc",
                "name": "Done",
                "idBoard": "1234567890abc",
            },
        ]
        return StubResponse(fake_response_data)

    if url == f"https://api.trello.com/1/boards/{test_board_id}/cards":
        fake_response_data = [
            {
                "id": "123abc",
                "idBoard": "1234567890abc",
                "idList": "456def",
                "name": "To Do Card 1",
            },
            {
                "id": "123def",
                "idBoard": "1234567890abc",
                "idList": "456def",
                "name": "To Do Card 2",
            },
            {
                "id": "123ghi",
                "idBoard": "1234567890abc",
                "idList": "456abc",
                "name": "Done Card",
            },
        ]
        return StubResponse(fake_response_data)

    raise Exception(f'Integration test did not expect URL "{url}"')


def test_index_page(monkeypatch, client):
    # #replaces any call to requests.get with our function ?
    monkeypatch.setattr(requests, "get", stub)
    response = client.get("/")
    assert response.status_code == 200
    assert "To Do Card 1" in response.data.decode()
