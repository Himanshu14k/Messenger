import pymongo
import pandas as pd
import json


class MongoDBManagement:

    def __init__(self, username, password):
        """
        This function sets the required url
        """
        try:
            self.username = username
            self.password = password
            self.url = 'mongodb+srv://{}:{}@cccluster.liy16i5.mongodb.net/test'.format(
                self.username, self.password)
        except Exception as e:
            raise Exception(
                f"(__init__): Something went wrong on initiation process\n" + str(e))

    def getMongoDBClientObject(self):
        """
        This function creates the client object for connection purpose
        """
        try:
            mongo_client = pymongo.MongoClient(self.url)
            return mongo_client
        except Exception as e:
            raise Exception(
                "(getMongoDBClientObject): Something went wrong on creation of client object\n" + str(e))

    def closeMongoDBconnection(self, mongo_client):
        """
        This function closes the connection of client
        :return:
        """
        try:
            mongo_client.close()
        except Exception as e:
            raise Exception(
                f"Something went wrong on closing connection\n" + str(e))

    def isDatabasePresent(self, db_name):
        """
        This function checks if the database is present or not.
        :param db_name:
        :return:
        """
        try:
            mongo_client = self.getMongoDBClientObject()
            if db_name in mongo_client.list_database_names():
                mongo_client.close()
                return True
            else:
                mongo_client.close()
                return False
        except Exception as e:
            raise Exception(
                "(isDatabasePresent): Failed on checking if the database is present or not \n" + str(e))

    def createDatabase(self, db_name):
        """
        This function creates database.
        :param db_name:
        :return:
        """
        try:
            database_check_status = self.isDatabasePresent(db_name=db_name)
            if not database_check_status:
                mongo_client = self.getMongoDBClientObject()
                database = mongo_client[db_name]
                mongo_client.close()
                return database
            else:
                mongo_client = self.getMongoDBClientObject()
                database = mongo_client[db_name]
                mongo_client.close()
                return database
        except Exception as e:
            raise Exception(
                f"(createDatabase): Failed on creating database\n" + str(e))

    def dropDatabase(self, db_name):
        """
        This function deletes the database from MongoDB
        :param db_name:
        :return:
        """
        try:
            mongo_client = self.getMongoDBClientObject()
            if db_name in mongo_client.list_database_names():
                mongo_client.drop_database(db_name)
                mongo_client.close()
                return True
        except Exception as e:
            raise Exception(
                f"(dropDatabase): Failed to delete database {db_name}\n" + str(e))

    def getDatabase(self, db_name):
        """
        This returns databases.
        """
        try:
            mongo_client = self.getMongoDBClientObject()
            # mongo_client.close()
            return mongo_client[db_name]
        except Exception as e:
            raise Exception(f"(getDatabase): Failed to get the database list")

    def getCollection(self, collection_name, db_name):
        """
        This returns collection.
        :return:
        """
        try:
            database = self.getDatabase(db_name)
            return database[collection_name]
        except Exception as e:
            raise Exception(
                f"(getCollection): Failed to get the database list.")

    def isCollectionPresent(self, collection_name, db_name):
        """
        This checks if collection is present or not.
        :param collection_name:
        :param db_name:
        :return:
        """
        try:
            database_status = self.isDatabasePresent(db_name=db_name)
            if database_status:
                database = self.getDatabase(db_name=db_name)
                if collection_name in database.list_collection_names():
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise Exception(
                f"(isCollectionPresent): Failed to check collection\n" + str(e))

    def createCollection(self, collection_name, db_name):
        """
        This function creates the collection in the database given.
        :param collection_name:
        :param db_name:
        :return:
        """
        try:
            collection_check_status = self.isCollectionPresent(
                collection_name=collection_name, db_name=db_name)
            if not collection_check_status:
                database = self.getDatabase(db_name=db_name)
                collection = database[collection_name]
                return collection
        except Exception as e:
            raise Exception(
                f"(createCollection): Failed to create collection {collection_name}\n" + str(e))

    def dropCollection(self, collection_name, db_name):
        """
        This function drops the collection
        :param collection_name:
        :param db_name:
        :return:
        """
        try:
            collection_check_status = self.isCollectionPresent(
                collection_name=collection_name, db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(
                    collection_name=collection_name, db_name=db_name)
                collection.drop()
                return True
            else:
                return False
        except Exception as e:
            raise Exception(
                f"(dropCollection): Failed to drop collection {collection_name}")

    def insertRecord(self, db_name, collection_name, record):
        """
        This inserts a record.
        :param db_name:
        :param collection_name:
        :param record:
        :return:
        """
        try:
            # collection_check_status = self.isCollectionPresent(
            #     collection_name=collection_name, db_name=db_name)
            # print(collection_check_status)
            # if collection_check_status:
            collection = self.getCollection(
                collection_name=collection_name, db_name=db_name)
            res = collection.insert_one(record)
            return res
            # else:
            #     print("collection No records")
            #     return f"collection not found"
        except Exception as e:
            raise Exception(
                f"(insertRecord): Something went wrong on inserting record\n" + str(e))

    def insertRecords(self, db_name, collection_name, records):
        """
        This inserts a record.
        :param db_name:
        :param collection_name:
        :param record:
        :return:
        """
        try:
            # collection_check_status = self.isCollectionPresent(collection_name=collection_name,db_name=db_name)
            # print(collection_check_status)
            # if collection_check_status:
            collection = self.getCollection(
                collection_name=collection_name, db_name=db_name)
            record = list(records.values())
            collection.insert_many(record)
            sum = 0
            return f"rows inserted "
        except Exception as e:
            raise Exception(
                f"(insertRecords): Something went wrong on inserting record\n" + str(e))

    def insertInEmbeddedRecord(self, db_name, collection_name, filter, subField, record, upsert=False):
        try:
            # collection_check_status = self.isCollectionPresent(
            #     collection_name=collection_name, db_name=db_name)
            # print(collection_check_status)
            # if collection_check_status:
            collection = self.getCollection(
                collection_name=collection_name, db_name=db_name)
            collection.update_one(
                filter, {'$push': {subField: record}}, upsert)
            return f"Record Inserted."
            # else:
            #     print("collection No records")
            #     return f"collection not found"
        except Exception as e:
            raise Exception(
                f"(insertInEmbeddedRecord): Something went wrong on inserting record\n" + str(e))

    def insertSlotRecord(self, db_name, collection_name, filter, record, upsert=False):
        try:
            # collection_check_status = self.isCollectionPresent(
            #     collection_name=collection_name, db_name=db_name)
            # print(collection_check_status)
            # if collection_check_status:
            collection = self.getCollection(
                collection_name=collection_name, db_name=db_name)
            collection.update_one(
                filter, {'$push': record}, upsert)
            return f"Record Inserted."
            # else:
            #     print("collection No records")
            #     return f"collection not found"
        except Exception as e:
            raise Exception(
                f"(insertInEmbeddedRecord): Something went wrong on inserting record\n" + str(e))

    def findfirstRecord(self, db_name, collection_name, query=None, includeField=None):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(
                collection_name=collection_name, db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(
                    collection_name=collection_name, db_name=db_name)
                firstRecord = collection.find_one(query, includeField)
                return firstRecord
        except Exception as e:
            raise Exception(
                f"(findRecord): Failed to find record for the given collection and database\n" + str(e))

    def findAllRecords(self, db_name, collection_name, includeField=None):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(
                collection_name=collection_name, db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(
                    collection_name=collection_name, db_name=db_name)
                findAllRecords = collection.find(projection=includeField)
                return findAllRecords
        except Exception as e:
            raise Exception(
                f"(findAllRecords): Failed to find record for the given collection and database\n" + str(e))
    
    def findLimitedRecords(self, db_name, collection_name, limit, includeField=None):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(
                collection_name=collection_name, db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(
                    collection_name=collection_name, db_name=db_name)
                findAllRecords = collection.find(projection=includeField).limit(limit)
                return findAllRecords
        except Exception as e:
            raise Exception(
                f"(findAllRecords): Failed to find limited record for the given collection and database\n" + str(e))

    def findRecordOnQuery(self, db_name, collection_name, query, includeField=None):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(
                collection_name=collection_name, db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(
                    collection_name=collection_name, db_name=db_name)
                findRecords = collection.find(query, includeField)
                return findRecords
        except Exception as e:
            raise Exception(
                f"(findRecordOnQuery): Failed to find record for given query,collection or database\n" + str(e))

    def aggregateRecord(self, db_name, collection_name, aggeregationQuery):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(
                collection_name=collection_name, db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(
                    collection_name=collection_name, db_name=db_name)
                findRecords = collection.aggregate(aggeregationQuery)
                return findRecords
        except Exception as e:
            raise Exception(
                f"(findRecordOnQuery): Failed to find record for given query,collection or database\n" + str(e))

    def getDistinctRecords(self, db_name, collection_name, field, filter):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(
                collection_name=collection_name, db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(
                    collection_name=collection_name, db_name=db_name)
                findRecords = collection.distinct(key=field, filter=filter)
                return findRecords
        except Exception as e:
            raise Exception(
                f"(getDistinctRecords): Failed to find record for given query,collection or database\n" + str(e))

    def updateOneRecordCompletely(self, db_name, collection_name, query):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(
                collection_name=collection_name, db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(
                    collection_name=collection_name, db_name=db_name)
                previous_records = self.findAllRecords(
                    db_name=db_name, collection_name=collection_name)
                new_records = query
                updated_record = collection.update_one(
                    previous_records, new_records)
                return updated_record
        except Exception as e:
            raise Exception(
                f"(updateRecord): Failed to update the records completely with given collection query or database name.\n" + str(
                    e))

    def updateOneRecordPartally(self, db_name, collection_name, filteredValue, newValue, upsert=False):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(
                collection_name=collection_name, db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(
                    collection_name=collection_name, db_name=db_name)
                if self.findfirstRecord(db_name=db_name, collection_name=collection_name, query=filteredValue):
                    updated_record = collection.update_one(
                        filteredValue, {"$set": newValue}, upsert=upsert)
                    return updated_record
                else:
                    return None
        except Exception as e:
            raise Exception(
                f"(updateOneRecordPartally): Failed to update the records partally with given collection query or database name.\n" + str(
                    e))

    def updateOneNestedRecordPartally(self, db_name, collection_name, filter, options, array_filters=None):
        """
        """
        try:
            collection = self.getCollection(
                collection_name=collection_name, db_name=db_name)
            updated_record = collection.update_one(
                filter=filter,
                update=options,
                array_filters=array_filters,
                upsert=False
            )
            return updated_record
        except Exception as e:
            raise Exception(
                f"(updateOneNestedRecordPartally): Failed to update the records partally with given collection query or database name.\n" + str(
                    e))

    def updateMultipleRecord(self, db_name, collection_name, query, newVal):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(
                collection_name=collection_name, db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(
                    collection_name=collection_name, db_name=db_name)
                updated_records = collection.update_many(
                    query, newVal, upsert=True)
                return updated_records
        except Exception as e:
            raise Exception(
                f"(updateMultipleRecord): Failed to update the records with given collection query or database name.\n" + str(
                    e))

    def deleteRecord(self, db_name, collection_name, query):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(
                collection_name=collection_name, db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(
                    collection_name=collection_name, db_name=db_name)
                collection.delete_one(query)
                return True
            return False
        except Exception as e:
            raise Exception(
                f"(deleteRecord): Failed to update the records with given collection query or database name.\n" + str(
                    e))

    def deleteRecords(self, db_name, collection_name, query):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(
                collection_name=collection_name, db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(
                    collection_name=collection_name, db_name=db_name)
                collection.delete_many(query)
                return "Multiple rows deleted"
        except Exception as e:
            raise Exception(
                f"(deleteRecords): Failed to update the records with given collection query or database name.\n" + str(
                    e))

    def deleteOneNestedRecordPartally(self, db_name, collection_name, filter, operations):
        """
        """
        try:
            collection = self.getCollection(
                collection_name=collection_name, db_name=db_name)
            deleted_record = collection.update_one(
                filter=filter,
                update=operations
            )
            return deleted_record
        except Exception as e:
            raise Exception(
                f"(deleteOneNestedRecordPartally): Failed to delete the records with given collection query or database name.\n" + str(
                    e))

    def deleteMultipleNestedRecords(self, db_name, collection_name, filter, operations):
        """
        """
        try:
            collection = self.getCollection(
                collection_name=collection_name, db_name=db_name)
            deleted_record = collection.update_many(
                filter=filter,
                update=operations
            )
            return deleted_record
        except Exception as e:
            raise Exception(
                f"(deleteMultipleNestedRecords): Failed to delete the records with given collection query or database name.\n" + str(
                    e))

    def getDataFrameOfCollection(self, db_name, collection_name):
        """
        """
        try:
            all_Records = self.findAllRecords(
                collection_name=collection_name, db_name=db_name)
            dataframe = pd.DataFrame(all_Records)
            return dataframe
        except Exception as e:
            raise Exception(
                f"(getDataFrameOfCollection): Failed to get DatFrame from provided collection and database.\n" + str(e))

    def saveDataFrameIntoCollection(self, collection_name, db_name, dataframe):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(
                collection_name=collection_name, db_name=db_name)
            dataframe_dict = json.loads(dataframe.T.to_json())
            if collection_check_status:
                self.insertRecords(collection_name=collection_name,
                                   db_name=db_name, records=dataframe_dict)
                return "Inserted"
            else:
                self.createDatabase(db_name=db_name)
                self.createCollection(
                    collection_name=collection_name, db_name=db_name)
                self.insertRecords(
                    db_name=db_name, collection_name=collection_name, records=dataframe_dict)
                return "Inserted"
        except Exception as e:
            raise Exception(
                f"(saveDataFrameIntoCollection): Failed to save dataframe value into collection.\n" + str(e))

    def getResultToDisplayOnBrowser(self, db_name, collection_name):
        """
        This function returns the final result to display on browser.
        """
        try:
            response = self.findAllRecords(
                db_name=db_name, collection_name=collection_name)
            result = [i for i in response]
            return result
        except Exception as e:
            raise Exception(
                f"(getResultToDisplayOnBrowser) - Something went wrong on getting result from database.\n" + str(e))
