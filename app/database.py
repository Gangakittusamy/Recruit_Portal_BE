import pymongo
from app.config import settings
def dbconnection():
    client =pymongo.MongoClient(settings.DATABASE_URL)
    print('Connected to MongoDB...')
    db = client[settings.MONGO_INITDB_DATABASE]
    return db

User = dbconnection().users
Form = dbconnection().forms
FormtableDates = dbconnection().formtabledates
UserLogos = dbconnection().userlogos
User.create_index([("email", pymongo.ASCENDING)], unique=True)
Form.create_index([("title", pymongo.ASCENDING)])
FormtableDates.create_index([("title", pymongo.ASCENDING)])