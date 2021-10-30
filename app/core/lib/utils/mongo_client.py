from pymongo import MongoClient, collection
from pymongo.database import Database

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class MongoWrapper():
    client = None
    def initialize(self) -> None:
        print('-- initializing mongo database --')
        self.client = MongoClient()
        print('-- insering test document --')
        result = self.get_database('face_recognition').get_collection('server').insert_one({
            'ok': True
        })
        print('-- successfully inserted test document --')
        self.get_database('face_recognition').get_collection('server').remove(result.inserted_id)
        print('-- successfully deleted test document --')

    def get_database(self, db_name: str)-> Database:
        return self.client.get_database(db_name)

    def get_collection(self, collection_name: str)-> collection.Collection:
        return self.get_database('face_recognition').get_collection(collection_name)