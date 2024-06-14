async def test_create(logged_in_ac, task_data):
    response = await logged_in_ac.post('/tasks', json=task_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"


async def test_create_unauthorized(ac, task_data):
    response = await ac.post('/tasks', json=task_data)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Unauthorized'}


async def test_create_wrong_parent_id(logged_in_ac, task_data):
    task_data['parent_task_id'] = 0
    response = await logged_in_ac.post('/tasks', json=task_data)
    assert response.status_code == 400
    assert response.json() == {'detail': 'Task with this id does not exist'}


async def test_create_wrong_employee_id(logged_in_ac, task_data):
    task_data['employee_id'] = 0
    response = await logged_in_ac.post('/tasks', json=task_data)
    assert response.status_code == 400
    assert response.json() == {'detail': 'Employee with this id does not exist'}


async def test_create_wrong_deadline(logged_in_ac, task_data):
    task_data['deadline'] = '2024-06-30T20:00'
    response = await logged_in_ac.post('/tasks', json=task_data)
    assert response.status_code == 422
    assert response.json()['detail'][0]["msg"] == 'Value error, deadline must be an aware datetime with timezone info'


async def test_get_all(ac):
    response = await ac.get('/tasks')
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_one(ac):
    response = await ac.get('/tasks/1')
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"


async def test_get_one_wrong_id(ac):
    response = await ac.get('/tasks/2')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task with this id not found'}


async def test_update(logged_in_ac):
    data = {
        "title": "Test Task Edited"
    }

    response = await logged_in_ac.patch('/tasks/1', json=data)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task Edited"


async def test_update_unauthorized(ac):
    data = {
        "title": "Test Task Edited"
    }

    response = await ac.patch('/tasks/1', json=data)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Unauthorized'}


async def test_update_wrong_id(logged_in_ac):
    data = {
        "title": "Test Task Edited"
    }

    response = await logged_in_ac.patch('/tasks/2', json=data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task with this id not found'}


async def test_delete_unauthorized(ac):
    response = await ac.delete('/tasks/1')
    assert response.status_code == 401
    assert response.json() == {'detail': 'Unauthorized'}


async def test_delete(logged_in_ac):

    response = await logged_in_ac.delete('/tasks/1')
    assert response.status_code == 204


async def test_delete_wrong_id(logged_in_ac):
    response = await logged_in_ac.delete('/tasks/2')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task with this id not found'}
