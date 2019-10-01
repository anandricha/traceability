import pymongo


class DB(object):
    URI = "mongodb://127.0.0.1:27017/"

    @staticmethod
    def init():
        client = pymongo.MongoClient(DB.URI)
        DB.DATABASE = client['traceability']

    @staticmethod
    def insert(collection, data):
        DB.DATABASE[collection].insert_one(data)

    @staticmethod
    def find(collection, query):
        return DB.DATABASE[collection].find(query)

    @staticmethod
    def distinct(collection, key) -> list:
        return DB.DATABASE[collection].distinct(key)

    @staticmethod
    def agrregate(collection, query)-> "iterable":
        print("result of aggregate --------",DB.DATABASE[collection].aggregate(query))
        return DB.DATABASE[collection].aggregate(query)

    @staticmethod
    def iterator_with_count(query_result_with_iterator,count_string) -> dict:
        if query_result_with_iterator._has_next() == False:
            return {count_string:"0"}
        else:
            for values in query_result_with_iterator:
                print("this value is available  in iterator----------",values)
                return values
    @staticmethod
    def iterator_with_group(query_result_with_iterator,count_string) -> dict:
        if query_result_with_iterator._has_next() == False:
            return {count_string:"0"}
        else:
            sprint_val= list()
            for values in query_result_with_iterator:
                val= list()
                val.append(values["_id"])
                val.append(values["count"])
                sprint_val.append(val)
            print("this is group data ",sprint_val)
            return  sprint_val