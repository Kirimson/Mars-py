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


def run(config_file):
    cnx = mysql.connector.connect(user='test', password='testpass',
                                  host='127.0.0.1',
                                  database='python')

    # Create the table for the sim if not made yet
    table_query = "create table if not exists mars ("
    for val_key in FIELD_TYPES:
        table_query += F"{val_key} {FIELD_TYPES[val_key]['type']} default {FIELD_TYPES[val_key]['default']}, "
    table_query += "result int)"
    cursor = cnx.cursor()

    execute(cursor, table_query)

    config = read_config(config_file)

    entrypoint.set_args(config)

    sim = entrypoint.GUIMain()

    col_names = ""
    col_vals = ""
    for val_key in config:
        if val_key != 'quiet':
            col_names += F"{val_key}, "
            col_vals += F"{config[val_key]}, "
    col_names += "result"
    col_vals += str(sim.step)
    insert_query = F"INSERT INTO mars ({col_names}) VALUES ({col_vals})"
    execute(cursor, insert_query)
    cnx.commit()

    cnx.close()


if __name__ == '__main__':
    run('config.json')
