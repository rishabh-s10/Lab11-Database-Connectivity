
import db

print("ADDING PERSON")

print("Rows inserted:", db.add_person(
    999999,
    "Test Person",
    "Production",
    "Available",
    "9876543210",
    "test@gmail.com",
    "1234567890"
))

print("\nDISPLAYING PEOPLE")

people = db.get_people()

for person in people:
    print(person)

print("\nUPDATING PERSON")

print("Rows updated:", db.update_person(
    999999,
    "Updated Person",
    "Technical",
    "Busy",
    "9876543210",
    "updated@gmail.com",
    "1234567890"
))

print("\nDELETING PERSON")

print("Rows deleted:", db.delete_person(999999))
