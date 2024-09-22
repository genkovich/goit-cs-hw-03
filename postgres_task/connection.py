import psycopg2

def connect():
    connection = psycopg2.connect(
        dbname='my_application',
        user='postgres',
        password='postgres',
        host='postgres',
        port='5432'
    )

    return connection
