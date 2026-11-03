
import psycopg2
from db_config import DB_SETTINGS

def connect():
    return psycopg2.connect(**DB_SETTINGS)


def add_person(person_id, name, department, availability, phone, email, emergency):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO person
        (person_id, full_name, department, availability, phone, email, emergency_contact)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (person_id, name, department, availability, phone, email, emergency))

    rows = cur.rowcount
    conn.commit()

    cur.close()
    conn.close()

    return rows


def get_people():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT person_id, full_name, department, availability,
        phone, email, emergency_contact
        FROM person
        ORDER BY person_id
    """)

    people = cur.fetchall()

    cur.close()
    conn.close()

    return people


def update_person(person_id, name, department, availability, phone, email, emergency):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        UPDATE person
        SET full_name=%s, department=%s, availability=%s,
            phone=%s, email=%s, emergency_contact=%s
        WHERE person_id=%s
    """, (name, department, availability, phone, email, emergency, person_id))

    rows = cur.rowcount
    conn.commit()

    cur.close()
    conn.close()

    return rows


def delete_person(person_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM person
        WHERE person_id=%s
    """, (person_id,))

    rows = cur.rowcount
    conn.commit()

    cur.close()
    conn.close()

    return rows


def test_connection():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT version()")
    print(cur.fetchone()[0])

    cur.close()
    conn.close()


if __name__ == "__main__":
    test_connection()
