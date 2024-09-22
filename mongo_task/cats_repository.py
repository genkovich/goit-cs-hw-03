import mongo_task.connection as connection
from mongo_task.cat import Cat

def list_cats():
    with connection.get_connection() as client:
        cats_cursor = client.my_application.cats.find({})
        return [Cat.from_dict(cat) for cat in cats_cursor]

def add_cat(cat):
    with connection.get_connection() as client:
        result = client.my_application.cats.insert_one(cat.to_dict())
        cat._id = result.inserted_id
        return result

def find_cat_by_name(name):
    with connection.get_connection() as client:
        data = client.my_application.cats.find_one({"name": name})
        if data:
            return Cat.from_dict(data)
        return None

def update_cat_by_name(name, cat_data):
    with connection.get_connection() as client:
        result = client.my_application.cats.update_one(
            {"name": name},
            {"$set": cat_data}
        )
        return result

def add_cat_feature(name, feature):
    with connection.get_connection() as client:
        result = client.my_application.cats.update_one(
            {"name": name},
            {"$push": {"features": feature}}
        )
        return result

def delete_cat_by_name(name):
    with connection.get_connection() as client:
        return client.my_application.cats.delete_one({"name": name})

def delete_all_cats():
    with connection.get_connection() as client:
        return client.my_application.cats.delete_many({})
