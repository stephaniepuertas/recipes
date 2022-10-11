

from flask_app.config.mysqlconnection import connectToMySQL

DATABASE = 'name_of_schema'


class Thing:
    def __init__(self, data):
        self.id = data['id']
        self.field1 = data['field1']
        self.field2 = data['field2']
        self.field3 = data['field3']
        self.field4 = data['field4']
        self.field5 = data['field5']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    def __repr__(self):
        return f'<Thing: {self.field1}>'

    # create a thing
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO things (field1, field2, field3, field4, field5) VALUES (%(field1)s, %(field2)s, %(field3)s, %(field4)s, %(field5)s);'
        thing_id = connectToMySQL(DATABASE).query_db(query, data)
        return thing_id

    # find all things (no data needed)
    @classmethod
    def find_all(cls):
        query = 'SELECT * from things;'
        results = connectToMySQL(DATABASE).query_db(query)
        things = []
        for result in results:
            things.append(Thing(result))
        return things

    # find one thing by id
    @classmethod
    def find_by_id(cls, data):
        query = 'SELECT * from things WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        thing = Thing(results[0])
        return thing

    # update one thing by id
    @classmethod
    def find_by_id_and_update(cls, data):
        query = 'UPDATE things SET field1 = %(field1)s, field2 = %(field2)s, field3 = %(field3)s, field4 = %(field4)s, field5 = %(field5)s WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True

    # delete one thing by id
    @classmethod
    def find_by_id_and_delete(cls, data):
        query = 'DELETE FROM things WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True