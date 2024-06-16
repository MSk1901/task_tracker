async def test_create(logged_in_ac, employee_data):
    response = await logged_in_ac.post('/employees', json=employee_data)

    assert response.status_code == 201
    assert response.json()['first_name'] == 'Ivan'


async def test_create_unauthorized(ac, employee_data):
    response = await ac.post('/employees', json=employee_data)

    assert response.status_code == 401
    assert response.json() == {'detail': 'Unauthorized'}


async def test_create_second(logged_in_ac, employee_data):
    response = await logged_in_ac.post('/employees', json=employee_data)

    assert response.status_code == 400
    assert response.json() == {'detail': 'User already has a registered employee'}


async def test_create_same_phone(logged_in_ac_2, employee_data):
    response = await logged_in_ac_2.post('/employees', json=employee_data)

    assert response.status_code == 400
    assert response.json() == {'detail': 'Employee with this phone number already exists'}


async def test_get_all(ac):
    response = await ac.get('/employees')

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_one(ac):
    response = await ac.get('/employees/1')

    assert response.status_code == 200
    assert response.json()['first_name'] == 'Ivan'


async def test_get_one_wrong_id(ac):
    response = await ac.get('/employees/2')

    assert response.status_code == 404
    assert response.json() == {'detail': 'Employee with this id not found'}


async def test_update(logged_in_ac):
    data = {
        'last_name': 'Petrov'
    }

    response = await logged_in_ac.patch('/employees/1', json=data)

    assert response.status_code == 200
    assert response.json()['last_name'] == 'Petrov'


async def test_update_wrong_dob(logged_in_ac):
    data = {
        'dob': '2024-10-25'
    }

    response = await logged_in_ac.patch('/employees/1', json=data)

    assert response.status_code == 422
    assert response.json()['detail'][0]["msg"] == 'Value error, Date of birth must be in the past'

    data = {
        'dob': '1900-10-25'
    }

    response = await logged_in_ac.patch('/employees/1', json=data)

    assert response.status_code == 422
    assert response.json()['detail'][0]["msg"] == "Value error, Date of birth can't be more than 100 years ago"


async def test_update_not_own(logged_in_ac_2):
    data = {
        'last_name': 'Sidorov'
    }

    response = await logged_in_ac_2.patch('/employees/1', json=data)

    assert response.status_code == 403
    assert response.json() == {'detail': 'Only the employee creator can perform this action'}


async def test_update_wrong_phone(logged_in_ac):
    data = {
        'phone': '12345'
    }

    response = await logged_in_ac.patch('/employees/1', json=data)

    assert response.status_code == 422
    assert response.json()['detail'][0]["msg"] == "String should match pattern '^\\+79\\d{9}$'"


async def test_delete(logged_in_ac):
    response = await logged_in_ac.delete('/employees/1')
    assert response.status_code == 204
