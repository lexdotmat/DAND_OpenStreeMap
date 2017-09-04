# https://sqlite.org/cli.html

# https://docs.python.org/2/library/sqlite3.html

import sqlite3
import pandas
# c = conn.cursor()

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



def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        # https://stackoverflow.com/questions/3425320/sqlite3-programmingerror-you-must-not-use-8-bit-bytestrings-unless-you-use-a-te
        conn.text_factory = str
        return conn
    except Error as e:
        print(e)

    return None

def create_table(conn, create_table_sql):
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

def import_csv(conn, table_name, csvfile):
    """ import a csv
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    df = pandas.read_csv (csvfile)
    df.to_sql (table_name, conn, if_exists='append', index=False)


def main ():
    database = "OSM_Basel_PART.db"

    """ creation of the strings to create the db
        Improvement: could be created from the schema.py file
        """
    # Node Table
    sql_create_node_table = """CREATE TABLE IF NOT EXISTS nodes (
                                    id integer ,
                                    lat float NOT NULL,
                                    lon float NOT NULL,
                                    user text NOT NULL,
                                    uid text NOT NULL,
                                    version integer NOT NULL,
                                    changeset integer NOT NULL,
                                    timestamp text
                                );"""
    # Node tags Table
    sql_create_node_tags_table = """ CREATE TABLE IF NOT EXISTS nodes_tags (
                                           id integer,
                                           key text,
                                           value text,
                                           type text
                                       ); """

    # Way Table
    sql_create_way_table = """ CREATE TABLE IF NOT EXISTS ways (
                                           id integer,
                                           user text,
                                           uid integer,
                                           version text,
                                           changeset integer,
                                           timestamp text
                                       ); """

    # way nodes Table
    sql_create_way_nodes_table = """ CREATE TABLE IF NOT EXISTS ways_nodes (
                                           id integer,
                                           node_id integer,
                                           position integer
                                       ); """

    # way tags Table
    sql_create_way_tags_table = """ CREATE TABLE IF NOT EXISTS ways_tags (
                                           id integer,
                                           key text,
                                           value text,
                                           type text
                                       ); """



    # create a database connection
    conn = create_connection(database)
    c = conn.cursor()
    if conn is not None:

        # create nodes table
        create_table (conn, sql_create_node_table)
        import_csv (conn, "nodes", "nodes.csv")

        # create tags table
        create_table (conn, sql_create_node_tags_table)
        import_csv(conn, "nodes_tags", "nodes_tags.csv")

        # create ways table
        create_table (conn, sql_create_way_table)
        import_csv(conn, "ways", "ways.csv")

        # create ways nodes table
        create_table (conn, sql_create_way_nodes_table)
        import_csv(conn, "ways_nodes", "ways_nodes.csv")

        # create way tags table
        create_table (conn, sql_create_way_tags_table)
        import_csv(conn, "ways_tags", "ways_tags.csv")

    else:
        print("Error! cannot create the database connection.")

## to run:
## sqlite OSM_Basel_PART.db
## .mode csv
## .import filename tablename
if __name__ == '__main__':
    main()

