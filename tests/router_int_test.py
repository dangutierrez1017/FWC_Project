import pytest
from src.controllers.routes import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Key Card" in response.data

def test_api_returns_data(client):
    response = client.get('/api/entries')
    assert response.status_code == 200
    data = response.get_json()
    assert "FirstName" in data[0]

def test_filter_by_name(client):
    response = client.get('/api/entries?name=Jean')
    assert response.status_code == 200
    data = response.get_json()
    assert all("jean" in (d["FirstName"].lower() + d["LastName"].lower()) for d in data)
