class ContactManager:
    def __init__(self):
        self.contacts = {}

    def validate_phone(self, phone):
        for char in phone:
            if not (char.isdigit() or char == '-' or char == '+'):
                return False
        return True

    def validate_email(self, email):
        if email == "":
            return True
        if '@' not in email or '.' not in email:
            return False
        return True

    def add_contact(self, name, phone, email=""):
        if name in self.contacts:
            return
        if not self.validate_phone(phone):
            print("Invalid phone number! Use only digits, hyphens and +.")
            return
        if not self.validate_email(email):
            print("Invalid email! Must contain @ and a period.")
            return
        self.contacts[name] = {"phone": phone, "email": email}
        print(f"Contact {name} added successfully!")

    def view_contact(self, name):
        if name not in self.contacts:
            print(f"Contact {name} not found.")
            return
        contact = self.contacts[name]
        print(f"Name: {name} | Phone: {contact['phone']} | Email: {contact['email']}")

    def update_contact(self, name, phone=None, email=None):
        if name not in self.contacts:
            print(f"Contact {name} not found.")
            return
        if phone:
            if not self.validate_phone(phone):
                print("Invalid phone number! Use only digits, hyphens and +.")
                return
            self.contacts[name]['phone'] = phone
        if email:
            if not self.validate_email(email):
                print("Invalid email! Must contain @ and a period.")
                return
            self.contacts[name]['email'] = email
        print(f"Contact {name} updated successfully!")

    def delete_contact(self, name):
        if name not in self.contacts:
            print(f"Contact {name} not found.")
            return
        del self.contacts[name]
        print(f"Contact {name} deleted successfully!")

    def search_contacts(self, query):
        query = query.lower()
        results = []
        for name, details in self.contacts.items():
            if (query in name.lower() or
                query in details['phone'] or
                query in details['email'].lower()):
                results.append((name, details))
        if not results:
            print(f"No contacts found for '{query}'.")
            return
        print(f"\n========== SEARCH RESULTS FOR '{query}' ==========")
        for name, details in results:
            print(f"Name: {name}")
            print(f"Phone: {details['phone']}")
            print(f"Email: {details['email']}")
            print("--------------------------------------------------")
        print(f"Total results found: {len(results)}")
        print("===================================================")

    def list_contacts(self):
        if not self.contacts:
            print("No contacts found.")
            return
        print("\n========== ALL CONTACTS ==========")
        for name, details in self.contacts.items():
            print(f"Name: {name} | Phone: {details['phone']} | Email: {details['email']}")
        print("===================================")


def main():
    manager = ContactManager()
    while True:
        print("\n=== Contact Manager Menu ===")
        print("1. Add Contact")
        print("2. View Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Search Contacts")
        print("6. List All Contacts")
        print("7. Exit")

        choice = input("Choose an option (1-7): ")

        if choice == "1":
            name = input("Enter name: ")
            phone = input("Enter phone number: ")
            email = input("Enter email (or press Enter to skip): ")
            manager.add_contact(name, phone, email)
        elif choice == "2":
            name = input("Enter name to view: ")
            manager.view_contact(name)
        elif choice == "3":
            name = input("Enter name to update: ")
            phone = input("Enter new phone (or press Enter to skip): ")
            email = input("Enter new email (or press Enter to skip): ")
            manager.update_contact(name, phone or None, email or None)
        elif choice == "4":
            name = input("Enter name to delete: ")
            manager.delete_contact(name)
        elif choice == "5":
            query = input("Enter search term: ")
            manager.search_contacts(query)
        elif choice == "6":
            manager.list_contacts()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose between 1-7.")

main()