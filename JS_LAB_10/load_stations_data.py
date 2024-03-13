import csv
import os
import mysql.connector


def gather_station_names():
    path_to_dir = '/Users/veraemelianova/PycharmProjects/JS_LAB_10/rentals2021'

    unique_station_names = set()

    for file_name in os.listdir(path_to_dir):
        if file_name.endswith('.csv'):
            path = os.path.join(path_to_dir, file_name)
            with open(path, 'r') as file:
                # print(file_name)
                csv_reader = csv.reader(file)
                next(csv_reader)
                for row in csv_reader:
                    unique_station_names.add(row[4])
                    unique_station_names.add(row[5])
    return unique_station_names


def load_stations(station_names, database_name):
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='28ver11ka2002',
        database=database_name)

    cursor = mydb.cursor()

    try:
        for station_id, station_name in enumerate(station_names):
            values = (station_id, station_name)
            sql = 'INSERT INTO Stations (station_id, station_name) VALUES (%s, %s)'
            cursor.execute(sql, values)

        mydb.commit()
        print('Data inserted successfully.')

    except mysql.connector.Error as err:
        print('Failed creating database: {}'.format(err))
        exit(1)
    finally:
        cursor.close()
        mydb.close()


names = gather_station_names()
# for id_s, name_s in enumerate(names):
#     print(id_s, name_s)
load_stations(names, 'bike_rentals')
