async def test_register(ac):
    data = {
        "email": "test@test.ru",
        "password": "Test"
    }

    response = await ac.post('auth/register', json=data)
    assert response.status_code == 201


async def test_login(ac):
    data = {
        "username": "test@test.ru",
        "password": "Test"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = await ac.post('auth/login', data=data, headers=headers)
    assert response.status_code == 204
    assert response.cookies is not None
