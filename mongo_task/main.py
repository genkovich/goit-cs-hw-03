from faker import Faker
from mongo_task.cat import Cat
import mongo_task.cats_repository as cats_repository


def execute():
    fake = Faker()
    for _ in range(10):
        cat = Cat(name=fake.name(), age=fake.random_int(min=1, max=20), features=[fake.word() for _ in range(3)])
        cats_repository.add_cat(cat)

    cats = cats_repository.list_cats()
    for cat in cats:
        print(cat)

    cat = cats_repository.find_cat_by_name(cats[0].name)
    print(cat)

    cats_repository.update_cat_by_name(cat.name, {"name": "new name", "age": 100, "features": ["new feature"]})

    cats_repository.add_cat_feature(cat.name, "new feature")

    cats_repository.delete_cat_by_name(cat.name)

    cats_repository.delete_all_cats()
