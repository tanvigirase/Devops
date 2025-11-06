def test_hello_route():
    from app.main import app
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello from OpenShift" in response.data
