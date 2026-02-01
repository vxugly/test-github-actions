from fastapi.testclient import TestClient



from src.main import app

from random import randint



client = TestClient(app)



# Существующие пользователи

users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]



UNEXISTS_USER = f'Jhone Doe_{str(randint(1234124, 2342142342))}'
UNIQ_EMAIL = f'uniqueEmail_{str(randint(23421342134, 12341234124124))}@test.com'



def test_get_existed_user():
    """Получение существующего пользователя"""
    response = client.get(
        "/api/v1/user",
        params=
        {
            'email': users[0]['email']
        }
    )

    assert response.status_code == 200
    assert response.json() == users[0]



def test_get_unexisted_user():
    """Получение несуществующего пользователя"""
    response = client.get("/api/v1/user", params={'email': 'unexisted@unknown.ru'})
    
    assert response.status_code == 404
    pass





def test_create_user_with_valid_email():
    """Создание пользователя с уникальной почтой"""
    unique_email = f'unique_{randint(1000000, 9999999)}@test.com'
    response = client.post(
        "/api/v1/user",
        json={
            'name': UNEXISTS_USER,
            'email': unique_email
        }
    )

    assert response.status_code == 201  # HTTP_201_CREATED вместо 200
    assert isinstance(response.json(), int)





def test_create_user_with_invalid_email():
    """Создание пользователя с почтой, которую использует другой пользователь"""
    response = client.post(
        "/api/v1/user",
        json={
            'name': UNEXISTS_USER,
            'email': users[0]['email']
        }
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}



def test_delete_user():
    """Удаление пользователя"""
    # Сначала создаем пользователя для удаления
    unique_email = f'delete_test_{randint(100000, 999999)}@test.com'



    # Создаем пользователя
    create_response = client.post(
        "/api/v1/user",
        json={
            'name': 'User to Delete',
            'email': unique_email
        }
    )

    assert create_response.status_code == 201



    # Удаляем пользователя
    delete_response = client.delete(
        "/api/v1/user",
        params={'email': unique_email}
    )

    assert delete_response.status_code == 204



    # Проверяем, что пользователь удален
    get_response = client.get("/api/v1/user", params={'email': unique_email})
    assert get_response.status_code == 404
