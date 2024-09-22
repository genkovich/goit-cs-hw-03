from postgres_task.connection import connect
import faker

def seed_statuses(db):
    db.execute("TRUNCATE TABLE status RESTART IDENTITY CASCADE")
    db.execute("INSERT INTO status (name) VALUES ('new')")
    db.execute("INSERT INTO status (name) VALUES ('in_progress')")
    db.execute("INSERT INTO status (name) VALUES ('completed')")

    db.connection.commit()

def seed_users(db):
    db.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE")
    fake = faker.Faker()
    for _ in range(10):
        db.execute(
            "INSERT INTO users (fullname, email) VALUES (%s, %s)",
            (fake.name(), fake.email())
        )
    db.connection.commit()

def seed_tasks(db):
    db.execute("TRUNCATE TABLE tasks RESTART IDENTITY CASCADE")
    fake = faker.Faker()
    for _ in range(50):
        db.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
            (fake.sentence(), fake.text(), fake.random_int(min=1, max=3), fake.random_int(min=1, max=10))
        )
    db.connection.commit()

def seed():
    db = connect()
    seed_statuses(db.cursor())
    seed_users(db.cursor())
    seed_tasks(db.cursor())
