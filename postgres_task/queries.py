from postgres_task.connection import connect


def run_queries():
    connection = connect()
    tasks = all_user_tasks(connection, 1)
    print(tasks)

    tasks = all_tasks_by_status(connection, 'new')
    print(tasks)

    update_task_status(connection, 1, 'in_progress')

    users = get_users_with_no_tasks(connection)
    print(users)

    add_task_for_user(connection, 1, 'New Task', 'New Task Description')

    tasks = get_incomplete_tasks(connection)
    print(tasks)

    delete_task_by_id(connection, 4)

    users = find_users_by_email(connection, '%@example.org')
    print(users)

    update_user_name(connection, 3, 'New Name')

    counts = get_task_count_by_status(connection)
    print(counts)

    tasks = get_tasks_by_user_email_domain(connection, '%@example.com')
    print(tasks)

    tasks = get_tasks_without_description(connection)
    print(tasks)

    results = get_users_and_tasks_by_status(connection, 'in_progress')
    print(results)

    results = get_users_and_task_counts(connection)
    print(results)


def all_user_tasks(db, user_id):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM tasks WHERE user_id = {user_id}")
    tasks = cursor.fetchall()
    return tasks

def all_tasks_by_status(db, status):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM tasks as t JOIN status as st ON t.status_id = st.id WHERE st.name = '{status}'")
    tasks = cursor.fetchall()
    return tasks

def update_task_status(db, task_id, new_status):
    cursor = db.cursor()
    cursor.execute(f"SELECT id FROM status WHERE name = '{new_status}'")
    status = cursor.fetchone()
    if not status:
        return False
    cursor.execute(f"UPDATE tasks SET status_id = {status[0]} WHERE id = {task_id}")
    db.commit()
    return True

def get_users_with_no_tasks(db):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM users u WHERE u.id NOT IN (SELECT DISTINCT user_id FROM tasks)")
    users = cursor.fetchall()
    return users

def add_task_for_user(db, user_id, task_name, task_description):
    cursor = db.cursor()
    query = """
    INSERT INTO tasks (user_id, title, description, status_id)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, task_name, task_description, 1))
    db.commit()
    return True

def get_incomplete_tasks(db):
    cursor = db.cursor()
    cursor.execute(f"SELECT t.* FROM tasks t JOIN status s ON t.status_id = s.id WHERE s.name != 'completed'")
    tasks = cursor.fetchall()
    return tasks

def delete_task_by_id(db, task_id):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM tasks WHERE id = {task_id}")
    db.commit()
    return True

def find_users_by_email(db, email_pattern):
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE email LIKE %s"
    cursor.execute(query, (email_pattern,))
    users = cursor.fetchall()
    return users

def update_user_name(db, user_id, new_name):
    cursor = db.cursor()
    query = "UPDATE users SET fullname = %s WHERE id = %s"
    cursor.execute(query, (new_name, user_id))
    db.commit()
    return True

def get_task_count_by_status(db):
    cursor = db.cursor()
    cursor.execute(f"SELECT s.name, COUNT(t.id) FROM status s LEFT JOIN tasks t ON t.status_id = s.id GROUP BY s.name")
    counts = cursor.fetchall()
    return counts

def get_tasks_by_user_email_domain(db, domain_pattern):
    cursor = db.cursor()
    query = """
    SELECT t.* FROM tasks t
    JOIN users u ON t.user_id = u.id
    WHERE u.email LIKE %s
    """
    cursor.execute(query, (domain_pattern,))
    tasks = cursor.fetchall()
    return tasks

def get_tasks_without_description(db):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM tasks WHERE description IS NULL OR description = ''")
    tasks = cursor.fetchall()
    return tasks

def get_users_and_tasks_by_status(db, status_name):
    cursor = db.cursor()
    query = """
    SELECT u.*, t.* FROM users u
    INNER JOIN tasks t ON u.id = t.user_id
    INNER JOIN status s ON t.status_id = s.id
    WHERE s.name = %s
    """
    cursor.execute(query, (status_name,))
    results = cursor.fetchall()
    return results

def get_users_and_task_counts(db):
    cursor = db.cursor()
    query = """
    SELECT u.*, COUNT(t.id) AS task_count FROM users u
    LEFT JOIN tasks t ON u.id = t.user_id
    GROUP BY u.id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    return results


