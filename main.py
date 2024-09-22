from postgres_task.migration import migration_execute
from postgres_task.seed import seed
from postgres_task.queries import run_queries

def main():
    migration_execute()
    seed()
    run_queries()



if __name__ == '__main__':
    main()
