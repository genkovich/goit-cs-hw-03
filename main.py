from postgres_task.migration import migration_execute
from postgres_task.seed import seed
from postgres_task.queries import run_queries
import mongo_task.main as cats_executor

def main():
    migration_execute()
    seed()
    run_queries()

    cats_executor.execute()



if __name__ == '__main__':
    main()
