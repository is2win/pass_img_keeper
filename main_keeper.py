from stegano import lsb
from PIL import Image
import ast
import datetime


def import_one_pass():
    """
    Запрашивает адрес сайта, логин и пароль. Преобразовывает в словарь
    :return: dict [str]
    """
    print("Введите_____")
    url = input("Сайт: ")
    login = input("Логин: ")
    password = input("Пароль: ")
    tmp_dict = {"URL": url, "Login": login, "Password": password}
    print("Вы добавили:")
    msg_with_pass(tmp_dict)
    return tmp_dict


def pass_input_importer():
    """
    Испортируем пользовательские запросы. Сначала вводим первый словарь, затем спрашиваем, нужно ли еще что-то вводить.
    Если нужно, добавляем в список еще пароль
    :return: list [dict[str]]
    """
    import_lst = []
    while True:
        import_lst.append(import_one_pass())
        ask_end = input("У вас еще остались пароли? (да/нет):\n").lower()
        positive_answers = ["да", "lf"]
        if ask_end not in positive_answers:
            break
    return import_lst


def import_new_pass():
    """
    Создаем правила импорта с выбором сценариев
    :return:
    """
    choose_type = str(input("Выбери правило импорта: 1-ввод пароля, 2-загрузка из файла\n"))
    if choose_type == '1':
        return pass_input_importer()
    else:
        pass


def import_img_and_code(pass_list, img_path_download, img_path_save, file_name):
    """
    Получаем список паролей, изображение для шифрования и путь для выхода
    :param pass_list:
    :param img_path_download:
    :param img_path_save:
    :return:
    """
    # Открываем изображение и кодируем сообщение
    secret_message = str(pass_list)
    encoded_image = lsb.hide(img_path_download, secret_message.encode("utf-8"))

    # Сохраняем измененное изображение
    encoded_image.save(img_path_save + file_name)


def decode_img(img_path_download):
    try:
        # Открываем измененное изображение и извлекаем сообщение
        encoded_image = Image.open(img_path_download)
        decoded_message = lsb.reveal(encoded_image)

        # Выводим извлеченное сообщение
        list_of_dicts = ast.literal_eval(decoded_message)
        return list_of_dicts
    except IndexError:
        print("ничего не спрятано в фотке")
        return []


def print_the_pass(pass_list):
    """
    Распечатыватель списка словарей
    :param pass_list:
    :return:
    """
    print("Пароли в файле")
    print("===============")
    for el in pass_list:
        msg_with_pass(el)


def msg_with_pass(tmp_dict):
    """
    Выводим текст используюя элементы словаря
    :param tmp_dict:
    :return:
    """
    print(f"Сайт: {tmp_dict.get('URL')}\nЛогин: {tmp_dict.get('Login')}\nПароль: {tmp_dict.get('Password')}")
    print(f"-----------------------")


def choose_global_scenario():
    """
    Глобальный сценарий для работы программы
    1 - делаем импорт паролей
    2 - декодируем пароли
    :return:
    """
    answer_work = input("Выбери: 1- закодировать файл, 2-расшифровать файл")
    img_path_download = input("Укажите путь до изображения")
    img_path_save = "img/"
    pass_in_old_file = decode_img(img_path_download)

    if answer_work == '1':
        pass_list = import_new_pass()
        if len(pass_in_old_file) > 0:
            for el in pass_in_old_file:
                pass_list.append(el)
        file_name = "img_" + str(datetime.datetime.now()) + ".png"
        import_img_and_code(pass_list, img_path_download, img_path_save, file_name)
        print_the_pass(pass_list)
    elif answer_work == '2':
        print_the_pass(pass_in_old_file)
    else:
        print(f"Не могу обработать запрос: {answer_work}")


def main():
    choose_global_scenario()


if __name__ == '__main__':
    main()