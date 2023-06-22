import requests
import os

from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

#Test1 - получение авторизационного ключа
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Тест получения ключа с существующим пользователем"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

#Test2 - получение списка питомцев пользователя
def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

#Test3 - добавление нового питомца без фото с верными вводными данными
def test_simple_add_new_pets_with_valid_key(name='Буся', animal_type='Русская голубая', age='3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.simple_adding_new_pet(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

#Test4 - обновление информации питомца из списка (последний добавленный)
def test_update_pet_with_valid_key(name='Хельма', animal_type='Немецкая овчарка', age=8):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Нет питомцев в списке")

#Test5 - удаление последнего добавленного питомца из списка пользователя
def test_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.simple_adding_new_pet(auth_key, "Буся", "кошка", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.delete_pet(auth_key, my_pets['pets'][0]['id'])
        assert status == 200
        assert pet_id not in my_pets.values()

    elif len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.delete_pet(auth_key, my_pets['pets'][0]['id'])
        assert status == 200
        assert pet_id not in my_pets.values()

#Test6 - добавление нового питомца с верными вводными данными
def test_add_new_pet_with_valid_data(name='Лютик', animal_type='Золотистый ретривер', age='0', pet_photo='images/golddog.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

#Test7 - добавление фото к существующему питомцу
def test_add_photo_pet_with_valid_data(pet_photo='images/cat.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)

    assert status == 200
    assert result['pet_photo'] != ''

#Test8 - добавление питомца с неверным ключом авторизации
def test_simple_add_new_pets_with_invalid_key(name='Буся', animal_type='Русская голубая', age='3'):
    auth_key = {'key': '9999999'}
    status, result = pf.simple_adding_new_pet(auth_key, name, animal_type, age)
    assert status == 403

#Test9 - добавление фото неверного формата к существующему питомцу
def test_add_photo_pet_with_invalid_data(pet_photo='images/netot.txt'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)

    assert status == 500

#Test10 - добавление нового питомца без фото с неверными вводными данными - БАГ! (даёт добавить)
def test_simple_add_new_pets_with_invalid_data(name=123456, animal_type='Русская голубая', age='3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.simple_adding_new_pet(auth_key, name, animal_type, age)
    assert status == 400

#Test11 - получение авторизационного ключа с несуществующим пользователем
def test_get_api_key_for_invalid_user(email='12sdfhj156', password='159247368'):
    """Тест получения ключа с существующим пользователем"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

#Test12 - обновление информации питомца из списка (последний добавленный) с неверным вводом возраста - БАГ (изменяет, статус 200)
def test_update_pet_with_invalid_age(name='Хельма', animal_type='Немецкая овчарка', age=123456789123456):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 400
        assert result['name'] == name
    else:
        raise Exception("Нет питомцев в списке")

#Test13 - получение списка питомцев по несуществующему фильтру
def test_get_list_of_pets_with_invalid_filter(filter='privet'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500

#Test14 - добавление нового питомца с пустыми вводными данными - БАГ, добавляет питомца с пустыми данными и фото
def test_add_new_pet_with_invalid_data(name='', animal_type='', age='', pet_photo='images/golddog.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400

#Test15 - получение списка питомцев пользователя
def test_get_user_pets_with_valid_key(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
