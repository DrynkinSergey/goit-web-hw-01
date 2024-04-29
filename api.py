from collections import UserDict
from datetime import datetime,timedelta
from abc import ABC, abstractmethod


def errors_handler(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
       
        except ValueError:
            print(
                f"Parameters is not correct... Invalid date format. Use DD.MM.YYYY ")
    return wrapper


def normalize_users_date(users_list, today=datetime.today()):
    """
    Функция нормализирует даты для корректной работы с разными годами рождения.

    :param users_list: Список пользователей
    :param today: Текущий день
    :return: Возвращается год пользователя приравнивая к текущему
    """
    return [{"name": user.name, "birthday": user.birthday.value.date()
    .replace(year=today.year)} for user in users_list if user.birthday]


def modified_users_date(date):
    """
    Функция хелпер для перевода поздравления на понедельник. Если день выпал на выходной
    :param date: День рождения пользователя
    :return: День поздравления
    """
    if date.weekday() in {5, 6}:
        return date + timedelta(days=7 - date.weekday())
    return date


def get_upcoming_birthdays(users_list: list) -> list:
    today = datetime.today()
    normalized_users = normalize_users_date(users_list)
    delta_max_period = today.date() + timedelta(days=7)
    delta_min_period = today.date() - timedelta(days=7)
    return[{"name": user['name'], "congratulation_date": modified_users_date(user['birthday']).strftime("%d.%m.%Y")}
           for user in normalized_users if delta_min_period <= user['birthday'] <= delta_max_period]


def command_parser(input_str: str):
    try:
        command, *args = input_str.lower().split()
        return command, *args
    except (TypeError, ValueError):
        print("Command is empty string...Try again!")


def greetings():
    return "Welcome to CLI assistant 🔥"


def help_api():
    return (
        "Available commands: \n"
        "- add name number\n"
        "- update name old_number new_number\n"
        "- delete name\n"
        "- all (saw all contacts)\n"
    )


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.value}"


class Birthday(Field):
    def __init__(self, value):
        if not self.is_valid_date_format(value):
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        self.value = datetime.strptime(value, "%d.%m.%Y")

    def is_valid_date_format(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False
    
    def __repr__(self):
        return f'{self.value.strftime("%d.%m.%Y")}'


class Name(Field): ...


class Phone(Field): ...


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        
    @errors_handler
    def add_birthday(self, value):
        self.birthday = Birthday(value)
    
    @errors_handler    
    def show_birthday(self):
        if not self.birthday:
            return print(f'Error')
        return print(f'{self.name.value} have birthday: {self.birthday.value.strftime("%d.%m.%Y")}')
    
    
    @staticmethod
    def phone_is_exist(data, phone):
        for p in data:
            if p.value == phone:
                return True

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                print(f"Phone {old_phone} edited to {new_phone}")
                break
        else:
            print(f"Phone {old_phone} is not exist!")

    def add_phone(self, phone):
        if self.phone_is_exist(self.phones, phone):
            return print("This number already exist")

        self.phones.append(Phone(phone))

    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value} \nPhones: {'; '.join(p.value for p in self.phones)}\nBirthday: {self.birthday.value.strftime("%d.%m.%Y")}\n"
        
        return f"Contact name: {self.name.value} \nPhones: {'; '.join(p.value for p in self.phones)}\nBirthday: {self.birthday}\n"


class AddressBook(UserDict):
    @errors_handler
    def birthdays(self):
        data = list(self.data.values())
        upcoming_birthdays = get_upcoming_birthdays(data)
        if len(upcoming_birthdays):
            print("Users with upcoming birthdays")
            print(upcoming_birthdays)
        else:
            print("No users with upcoming birthdays")

    def add_record(self, record):
        self.data[record.name] = record

    def find_record(self, target):
        for i in self.data.values():
            if i.name.value.lower() == target.lower():
                return i

    def show(self):
        if len(self.data) == 0:
            print("No data exist!")
        for record in self.data.values():
            print(record)

    def remove(self, target):
        for record in list(self.data.keys()):
            if record.value == target:
                del self.data[record]
                print(f"User {target} has been deleted!")
