# https://sqlite.org/cli.html

# https://docs.python.org/2/library/sqlite3.html

import sqlite3

c = conn.cursor()

schema = {
    'node': dict (type='dict', schema={
        'id': {'required': True, 'type': 'integer', 'coerce': int},
        'lat': {'required': True, 'type': 'float', 'coerce': float},
        'lon': {'required': True, 'type': 'float', 'coerce': float},
        'user': {'required': True, 'type': 'string'},
        'uid': {'required': True, 'type': 'integer', 'coerce': int},
        'version': {'required': True, 'type': 'string'},
        'changeset': {'required': True, 'type': 'integer', 'coerce': int},
        'timestamp': {'required': True, 'type': 'string'}
    }),
    'node_tags': dict (type='list', schema={
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'key': {'required': True, 'type': 'string'},
            'value': {'required': True, 'type': 'string'},
            'type': {'required': True, 'type': 'string'}
        }
    }),
    'way': dict (type='dict', schema={
        'id': {'required': True, 'type': 'integer', 'coerce': int},
        'user': {'required': True, 'type': 'string'},
        'uid': {'required': True, 'type': 'integer', 'coerce': int},
        'version': {'required': True, 'type': 'string'},
        'changeset': {'required': True, 'type': 'integer', 'coerce': int},
        'timestamp': {'required': True, 'type': 'string'}
    }),
    'way_nodes': dict (type='list', schema={
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'node_id': {'required': True, 'type': 'integer', 'coerce': int},
            'position': {'required': True, 'type': 'integer', 'coerce': int}
        }
    }),
    'way_tags': dict (type='list', schema={
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'key': {'required': True, 'type': 'string'},
            'value': {'required': True, 'type': 'string'},
            'type': {'required': True, 'type': 'string'}
        }
    })
}

# Creation of the database

# code adapted from http://www.sqlitetutorial.net/sqlite-python/create-tables/

# Extract Creation commands from the schema



def create_connection (db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect (db_file)
        return conn
    except Error as e:
        print(e)

    return None

def create_table(conn, create_table_sql)
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main ():
    database = "OSM_Basel_PART.db"

    sql_create_node_table = """CREATE TABLE IF NOT EXISTS node (
                                    id integer PRIMARY KEY,
                                    lat float NOT NULL,
                                    lon float NOT NULL,
                                    user text NOT NULL,
                                    uid text NOT NULL,
                                    version integer NOT NULL,
                                    changeset integer NOT NULL,
                                    timestamp text
                                );"""

    sql_create__node_tags_table = """ CREATE TABLE IF NOT EXISTS projects (
                                           id integer PRIMARY KEY,
                                           name text NOT NULL,
                                           begin_date text,
                                           end_date text
                                       ); """
    # create a database connection
    conn = create_connection (database)
    if conn is not None:
        # create projects table
        create_table (conn, sql_create_node_table)
        # create tasks table
        create_table (conn, sql_create_tasks_table)

    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()

