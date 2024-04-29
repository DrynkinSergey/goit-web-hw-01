from api import (
    Record,
    AddressBook,
    get_upcoming_birthdays,
    greetings,
    help_api,
    command_parser,
    normalize_users_date,
)
import pickle
from abc import ABC, abstractmethod


class UserInterface(ABC):
    @abstractmethod
    def show_message(self, message):
        pass


class CLIUserInterface(UserInterface):
    def show_message(self,message):
        print(message)


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def main():
    book = load_data()
    cli = CLIUserInterface()
    exit_commands = ["q", "quit", "exit", "leave", "left"]
    cli.show_message('Welcome to assistant bot! You can use "help" command to see more')

    while True:
        params = input(">>>  ")
        if not params:
            cli.show_message("Please, enter not empty string! ")
            continue

        command, *args = command_parser(params)
        if len(args) != 0:
            name = args[0]

        match (command):
            case "hello" | "start":
                cli.show_message(greetings())

            case "add" | "create":
                if len(args) < 2:
                    cli.show_message("Please enter, correct args. Example: 'add Oleh 0932244555'")
                    continue
                new_contact = Record(name)
                exist_record = book.find_record(name)
                if exist_record:
                    exist_record.add_phone(args[1])
                else:
                    new_contact.add_phone(args[1])
                    book.add_record(new_contact)

            case "find" | "get":
                exist = book.find_record(name)
                cli.show_message(exist)

            case "birthdays" | "b":
                book.birthdays()

            case "show_birthday":
                if len(args) < 1:
                    cli.show_message("Please enter, correct args. Example: 'show_birthday Oleh'")
                    continue
                exist_record = book.find_record(name)
                if exist_record:
                    exist_record.show_birthday()
                else:
                    cli.show_message("User is not exist")

            case "add_birthday":
                if len(args) < 2:
                    cli.show_message(
                        "Please enter, correct args. Example: 'add_birthday Oleh 22.03.2024'"
                    )

                    continue
                exist_record = book.find_record(name)
                if exist_record:
                    exist_record.add_birthday(args[1])
                else:
                    cli.show_message(
                        "User is not exist. Please, add user first. Example: 'add_birthday Oleh 22.03.2024'"
                    )

            case "update":
                if len(args) < 3:
                    cli.show_message(
                        "Please enter, correct args. Example: 'update Oleh 0932244555 05012345678'"
                    )
                    continue
                exist = book.find_record(name)
                if exist:
                    exist.edit_phone(args[1], args[2])
                else:
                    cli.show_message(f'User "{name}" is not found')

            case "delete" | "del":
                book.remove(name)

            case "all" | "show":
                book.show()

            case "help" | "info":
                print(help_api())

            case command if command in exit_commands:
                save_data(book)
                cli.show_message("Bye!")
                break
            case _:
                cli.show_message("Invalid command! Try again...\n")


if __name__ == "__main__":
    main()
