from pymongo import  MongoClient

token = '5767287336:AAHfUudWHmWDlg304-KhzrNXBnVXAejEUoA'

client = MongoClient("localhost:27017")
db = client["autoservis"]


def insert_data_to_mongodb(data, collection_name):
    """Добавляет данные в коллекцию"""
    
    collection = db[collection_name]

    # Вставка данных в коллекцию
    collection.insert_one(data)
    

'''# Пример 
user_data = {
    "name": "John",
    "age": 25,
    "city": "New York"
}'''



def get_value_from_mongodb(collection_name, filter_query, field_name):
    """Принимает название коллекции, фильтр запроса и название поля, значение которого нужно получить"""
    """user_filter = {"name": "John"}"""
    """пример : user_age = get_value_from_mongodb("users", user_filter, "age")"""
    
    collection = db[collection_name]

    # Запрос значения из коллекции
    value = collection.find_one(filter_query, {field_name: 1})
    if value:
        return value[field_name] # возвращаем значение поля
    else:
        return None


# Пример использования функции
"""user_filter = {"user_ID": 5075691809}
Firstname = get_value_from_mongodb("users", user_filter, "gosnumber")
print(Firstname)"""


def check_object_existence(collection_name, object_id): 
    """Проверяет наличие объекта в коллекции"""
    # Принимает название коллекции и идентификатор объекта,
    # который нужно проверить на наличие

    collection = db[collection_name]

    # Проверка наличия объекта с указанным ID
    count = collection.count_documents({"_id": object_id})
    return count > 0




def get_collection_count(collection_name): 
    """Принимает название коллекции и возвращает количество объектов в коллекции"""
    
    collection = db[collection_name]

    # Получение количества объектов в коллекции
    count = collection.count_documents({})
    return count


def get_object_from_mongodb(collection_name, filter_query):
    """Принимает название коллекции и фильтр запроса и возвращает объект из коллекции"""

    
    collection = db[collection_name]

    # Получение объекта из коллекции
    obj = collection.find_one(filter_query)
    return obj

