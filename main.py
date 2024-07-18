from csv import DictWriter, DictReader  # импорт модулей для работы со словарями из библиотеки csv
from os.path import exists  # импорт модуля проверки существования файла


class MyNameError(Exception):  # собственный класс исключений
    def __init__(self, txt):
        self.txt = txt

def copy_line(source_file, source_line_number, destination_file, destination_line_number):
    with open(source_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        source_line = lines[source_line_number - 1]

    with open(destination_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines[destination_line_number - 1] = source_line

    with open(destination_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def get_data():  # функция получения с консоли данных о человеке и его номере телефона
    flag = False  # необходимо для работы цикла, который ниже
    while not flag:  # цикл работает, пока не получит значение False, см. выше
        try:  # проверка валидности вводимых данных
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise MyNameError("Слишком короткое имя")
            last_name = input("Введите имя: ")
            if len(last_name) < 5:
                raise MyNameError("Слишком короткая фамилия")
            phone = input("Введите номер телефона: ")
            if len(phone) < 11:
                raise MyNameError("Номер телефона должен быть не менее 11 символов")
        except MyNameError as err:  # если исключение сработало, то выводим сообщение об ошибке
            print(err)
        else:
            flag = True  # меняем значение flag на True, соответственно, это означает выход из цикла
    return [first_name, last_name, phone]  # по итогу работы функции возвращаем список


def create_file(filename):  # функция создания файла csv
    with open(filename, 'w', encoding='utf-8') as data:  # открываем файл для записи (w) и указываем его кодировку
        f_w = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])  # создаем объект DictWriter
        f_w.writeheader()  # пишем в файл заголовки


def read_file(filename):  # функция чтения файла
    with open(filename, 'r', encoding='utf-8') as data:  # открываем файл для чтения (r) и указываем его кодировку
        f_r = DictReader(data)  # создаем объект DictWriter
        return list(f_r)  # возвращаем список словарей


def write_file(filename, lst):  # функция записи в файл, filename - имя файла, lst - список из функции get_data()
    res = read_file(filename)  # читаем файл функцией read_file(), получаем список словарей
    obj = {'Имя': lst[0], 'Фамилия': lst[1], 'Телефон': lst[2]}  # формируем значения словаря, используя список
    res.append(obj)  # добавляем сформированный словарь к списку
    standard_write(filename, res)  # записываем изменения в файл при помощи вызова функции standard_write()


def row_search(filename):  # поиск по файлу csv
    last_name = input("Введите фамилию: ")  # что ищем
    res = read_file(filename)  # читаем файл функцией read_file(), получаем список словарей
    for row in res:  # помним у нас список словарей, проходим по ним в цикле
        if last_name == row['Фамилия']:  # сравниваем значение того что ищем (last_name)
            # со значением словаря по ключу Фамилия
            return row  # возвращаем найденный словарь, он же одна строка из файла, он же одна запись файла
    return "Запись не найдена"  # возвращаем это, если не нашли ничего подходящего


def delete_row(filename):  # функция удаления строки из файла
    row_number = int(input("Введите номер строки: "))  # номер строки в целочисленном формате
    res = read_file(filename)  # читаем файл функцией read_file(), получаем список словарей
    res.pop(row_number - 1)  # удаляем словарь с номером меньше чем row_number на 1, т.к. индексы списка стартуют с 0
    standard_write(filename, res)  # записываем изменения в файл при помощи вызова функции standard_write()


def standard_write(filename, res):  # функция записи в файл csv, res - список из функции get_data()
    with open(filename, 'w', encoding='utf-8') as data:  # открываем файл для записи (w) и указываем его кодировку
        f_w = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])  # создаем объект DictWriter
        f_w.writeheader()  # пишем в файл заголовки
        f_w.writerows(res)  # пишем строки, res - список словарей, каждый из которых - отдельная строка файла


def change_row(filename):  # функция изменения строки в csv файле
    row_number = int(input("Введите номер строки: "))  # номер строки в целочисленном формате
    res = read_file(filename)  # читаем файл функцией read_file(), получаем список словарей
    data = get_data()  # вызываем функцию get_data() и получаем список словарей
    res[row_number - 1]["Имя"] = data[0]  # меняем все данные в указанной выше строке, переменная row_number
    res[row_number - 1]["Фамилия"] = data[1]
    res[row_number - 1]["Телефон"] = data[2]
    standard_write(filename, res)  # записываем изменения в файл при помощи вызова функции standard_write()
    

def main():  # основной модуль с которого начинает работу программа
    while True:  # бесконечный цикл, в котором ожидаем реакции с консоли
        print('Сделайте выбор: "q"- завершение; "w"-запись csv; "r"-чтение csv; "f"-поиск в csv', end=';')
        print(' "d"-удаление из csv; "c"-изменить строку в csv; "p"-Перенести строку из одного файла в другой.')
        command = input("Укажите ваш выбор: ")
        if command == "q":
            break
        elif command == "w":
            if not exists(filename):  # если файл с указанным именем не существует,
                create_file(filename)  # то создаем его, вызвав функцию create_file()
            write_file(filename, get_data())
        elif command == "r":
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            print(read_file(filename))
        elif command == "f":
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            print(row_search(filename))
        elif command == "d":
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            delete_row(filename)
        elif command == "c":
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            change_row(filename)
        elif command == "p":
            source_file = input("Укажате файл с которого надо перенести строку: ")
            if not exists(source_file):
                print("Файл не существует.")
            continue
            destination_file = input("Укажате файл в который нужно перенести строку: ")
            if not exists(destination_file):
                print("Файл не существует.")
            continue
            line_number_to_read = int(input("Укажате номер строки для копирования:  "))
            line_number_to_replace = int(input("Укажате номер строки для замены:  "))
            copy_line(source_file, line_number_to_read, destination_file, line_number_to_replace)

filename = 'phone.csv'  # задаем имя файла csv в переменную
main()  # вызов функции с основным модулем выбора
