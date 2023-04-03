import pytest
from api import PetFriends
from setting import valid_email, valid_password, invalid_password, invalid_email
import os


pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_whith_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Бэтти', animal_type='биверйорк',
                                     age='1', pet_photo='images/biver.jpeg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Бэтти", "йорк", "1", "images/biver.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='йорк', age=0):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
    # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_not_give_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    """Проверяем, что запрос api ключа с неверным паролем не выполняется и дает статус 403"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' in result


def test_not_give_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    """Проверяем, что запрос api ключа с неверным форматом почты не выполняется и дает статус 403"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' in result


def test_add_new_pet_with_invalid_data(name='Бэтти', animal_type='биверйорк',
                                     age='2000', pet_photo='images/biver.jpeg'):
    """Проверяем, что нельзя добавить питомца с некорректными данными - некоректное значение поля возраст"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403
    assert result['name'] == name
    # Тест показывает fail и статус 200, значит добавить питомца с некорректным значением возраста получается
    # это баг


def test_add_new_pet_with_invalid_data_negative_age(name='Бэтти', animal_type='биверйорк',
                                     age='-2', pet_photo='images/biver.jpeg'):
    """Проверяем, что нельзя добавить питомца с некорректными данными - отрицательное значение возраста"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403
    assert result['name'] == name
    # Тест показывает fail и статус 200, значит добавить питомца с отрицательным значением возраста получается
    # это баг


def test_add_new_pet_simple_with_valid_data(name='Сырник', animal_type='кот',
                                     age='5'):
    """Проверяем что можно добавить питомца без фото с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_pet_photo_with_valid_data(pet_photo='images/cheese.jpeg'):
    """Проверяем, что можно добавить фотографию к уже существующему питомцу"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.set_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200
        assert status == 200
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_new_pet_with_invalid_data_photo(name='Бэтти', animal_type='биверйорк',
                                     age='1', pet_photo='images/biver.txt'):
    """Проверяем что нельзя добавить питомца с корректными данными - неверный формат фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 415
    assert result['name'] == name
# тест не прошел, результат "не найден файл" потому что указан неверный формат


def test_add_new_pet_with_invalid_data_animal_type(name='Бэтти', animal_type='<b@вер',
                                     age='1', pet_photo='images/biver.jpeg'):
    """Проверяем что нельзя добавить питомца с корректными данными - спецсимволы в поле вид животного"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert result['name'] == name
#тест ен прошел так как добавить животное с спецсимволами в поле вид животного возможно и статус 200!!
# 403!=200  это баг


def test_get_all_pets_whith_invalid_key(filter=''):
    """Проверяем, что запрос списка всех питомцев c не валидным ключом выдает статус 403"""

    auth_key = {'key': '12345'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403


def test_add_new_pet_simple_with_nonedata(name='', animal_type='',
                                            age=''):
    """Проверяем что нельзя добавить питомца с пустыми полями"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
# оставила статус 200, что бы отследить что питомца можно добавить с пустыми полями, поэтому это баг
