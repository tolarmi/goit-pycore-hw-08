import pickle
from datetime import datetime

class Field:
    pass

class Name(Field):
    def __init__(self, value):
        self.value = value

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format. Please enter a 10-digit number.")
        self.value = value

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_record(self, record):
        self.contacts.append(record)

    def find(self, name):
        for contact in self.contacts:
            if contact.name.value.lower() == name.lower():
                return contact
        return None

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for contact in self.contacts:
            if contact.birthday:
                birthday_date = contact.birthday.value.replace(year=today.year)
                if birthday_date < today:
                    birthday_date = birthday_date.replace(year=today.year + 1)
                days_until_birthday = (birthday_date - today).days

                if 0 < days_until_birthday <= 7:
                    upcoming_birthdays.append({"name": contact.name.value, "birthday_date": birthday_date.strftime("%Y.%m.%d")})

        return upcoming_birthdays

    def save_data(self, filename="addressbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.contacts, f)

    def load_data(self, filename="addressbook.pkl"):
        try:
            with open(filename, "rb") as f:
                self.contacts = pickle.load(f)
        except FileNotFoundError:
            self.contacts = []

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
    return inner

@input_error
def add(args, book):
    name, phone = args
    record = book.find(name)
    if record:
        record.add_phone(phone)
        return "Phone number updated."
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."

@input_error
def change(args, book):
    name, phone = args
    record = book.find(name)
    if record:
        record.add_phone(phone)
        return "Phone number updated."
    else:
        return "Contact not found."

@input_error
def phone(args, book):
    name, *_ = args
    record = book.find(name)
    if record:
        return f"Phone number for {name}: {', '.join([phone.value for phone in record.phones])}"
    else:
        return "Contact not found."

@input_error
def all_contacts(args, book):
    if not book.contacts:
        return "No contacts found."
    else:
        return "\n".join([f"{contact.name.value}: {', '.join([phone.value for phone in contact.phones])}" for contact in book.contacts])

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        return "Contact not found."

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record and record.birthday:
        return f"Birthday for {name}: {record.birthday.value.strftime('%d.%m.%Y')}"
    elif record and not record.birthday:
        return f"No birthday set for {name}."
    else:
        return "Contact not found."

@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join([f"{contact['name']}'s birthday on {contact['birthday_date']}" for contact in upcoming_birthdays])
    else:
        return "No upcoming birthdays."

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    book.load_data()

    while True:
        user_input = input("Enter a command: ").strip().lower()
        command, *args = user_input.split()

        if command in ["close", "exit"]:
            book.save_data()
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add(args, book))
        elif command == "change":
            print(change(args, book))
        elif command == "phone":
            print(phone(args, book))
        elif command == "all":
            print(all_contacts(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
