#!/usr/bin/env python3
import main as entrypoint
import mysql.connector
import json


FIELD_TYPES = {
    'seed': {'type': 'int', 'default': entrypoint.ModelConstants.seed},
    'width': {'type': 'int', 'default': entrypoint.ModelConstants.width},
    'depth': {'type': 'int', 'default': entrypoint.ModelConstants.depth},
    'rocks': {'type': 'int', 'default': entrypoint.ModelConstants.rock_count},
    'clusters': {'type': 'int', 'default': entrypoint.ModelConstants.cluster_count},
    'std': {'type': 'double', 'default': entrypoint.ModelConstants.std},
    'obstacle': {'type': 'double', 'default': entrypoint.ModelConstants.obstacle_chance},
    'vehicle': {'type': 'double', 'default': entrypoint.ModelConstants.vehicle_chance},
}


def read_config(config_file):
    with open(config_file, 'r') as f:
        data = json.loads(f.read())
    return data


def execute(cursor, query):
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print(err)
    return cursor


def run(config_file):
    cnx = mysql.connector.connect(user='mars', password='marspass',
                                  host='127.0.0.1',
                                  port=3309,
                                  database='marsdb')

    # Create the table for the sim if not made yet
    table_query = "create table if not exists mars (id int(11) not null auto_increment, "
    for val_key in FIELD_TYPES:
        table_query += F"{val_key} {FIELD_TYPES[val_key]['type']} default {FIELD_TYPES[val_key]['default']}, "
    table_query += "result int, constraint id primary key (id))"
    cursor = cnx.cursor()

    execute(cursor, table_query)

    config = read_config(config_file)

    entrypoint.set_args(config)

    # Check if done already
    select = "select result from mars where "
    fields = FIELD_TYPES.copy() 
    for val_key in config:
        if val_key != 'quiet':
            fields[val_key]['default'] = config[val_key]
    for i, val_key in enumerate(fields):
        select += F"{val_key}={fields[val_key]['default']}"
        if i < len(fields) - 1:
            select += " and "

    execute(cursor, select)

    result = None
    for db_result in cursor:
        result = db_result[0]
    
    if not result:
        sim = entrypoint.GUIMain()
        result = sim.step
        col_names = ""
        col_vals = ""
        for val_key in config:
            if val_key != 'quiet':
                col_names += F"{val_key}, "
                col_vals += F"{config[val_key]}, "
        col_names += "result"
        col_vals += str(result)
        insert_query = F"INSERT INTO mars ({col_names}) VALUES ({col_vals})"
        execute(cursor, insert_query)
        cnx.commit()

    cnx.close()

    print(result)


if __name__ == '__main__':
    run('config.json')
