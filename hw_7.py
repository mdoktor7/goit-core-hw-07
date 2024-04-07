from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise ValueError("Phone number must be 10 digits.")


class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            print("Birthday must have format day.month.year")


class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)   

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_phone_number, new_phone_number):
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number

    def add_birthday(self, birthday):
        if self.birthday is None:
            self.birthday = Birthday(birthday)
        else:
            raise ValueError("Only one birthday can be added.")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days=7):
        today = datetime.today().date()
        upcoming_birthdays = {}
        for name, user in self.data.items():
            birthday = datetime.strptime(user['birthday'], '%Y.%m.%d').date()
            birthday_this_year = birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
            days_before_birthday = (birthday_this_year - today).days
            if days_before_birthday <= 7:
                if birthday_this_year.weekday() >= 5:
                    birthday_this_year += timedelta(days - birthday_this_year.weekday())
                upcoming_birthdays[name] = birthday_this_year.strftime("%Y.%m.%d")

        return upcoming_birthdays


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please." 
        except KeyError:
            return "Contact not found."
        except IndexError:    
            return "Invalid command format."
    return inner 


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, phone = args
    book[name] = phone
    return "Contact updated successfully" 


@input_error
def show_contact(args, book: AddressBook):
    name = args[0]
    return book[name]
    

@input_error
def show_all_contacts(args, book: AddressBook):
    for name, phone in book.items():
        print(f"{name}: {phone}")
    if not book:
        return "No contacts found."


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    book[name] = birthday
    return "Birthday added."
  

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    return book[name]


@input_error
def birthdays(book: AddressBook):
    for name, birthday in book.items():
        print(f"{name}: {birthday}")
    if not book:
        return "No birthdays found."


@input_error
def get_upcoming_birthdays(book: AddressBook):
    for name, birthday in book.items():
        print(f"{name}: {birthday}")
    if not book:
        return "No contacts found."


@input_error
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command:")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            return False

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "show":
            print(show_contact(args, book))

        elif command == "all":
            print(show_all_contacts(args, book))

        elif command == "hello":
            print("How can I help you?")
       
        elif command == "add-birthday":
            print(add_birthday(args, book))
        
        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(get_upcoming_birthdays(args, book))

        else:
            print("Invalid command.")
        

if __name__ == "__main__":
    main()
