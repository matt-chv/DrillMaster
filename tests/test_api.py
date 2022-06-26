#for future consider using pytest
#https://testdriven.io/blog/flask-pytest/

def test_students():
    """
    
    """
    import requests
    response = requests.get('/students')
    data = response.json()
    
    assert response.status_code == 200
    assert "deck" in data[0]
    assert data[0]["deck"]=="demo"
