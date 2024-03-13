import sys
import mysql.connector


def create_database(database_name):
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='28ver11ka2002')
    cursor = mydb.cursor()

    try:
        cursor.execute('CREATE DATABASE ' + database_name)
        print('Database ' + database_name + ' created successfully')

        mydb.database = database_name

        # with open(file_name, 'r') as file:
        #     sql_file = file.read()

        cursor.execute('CREATE TABLE if not exists Stations (station_id INT PRIMARY KEY,station_name VARCHAR(255));')
        cursor.execute('CREATE TABLE if not exists Rentals (rental_id INT PRIMARY KEY,bike_number INT,start_time TIMESTAMP,end_time TIMESTAMP,rental_station INT REFERENCES Stations(station_id),return_station INT REFERENCES Stations(station_id));')
        print('Tables created successfully')

    except mysql.connector.Error as err:
        print('Failed creating database: {}'.format(err))
        exit(1)

    finally:
        cursor.close()
        mydb.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 create_database.py database_name')
        exit(1)
    else:
        create_database(sys.argv[1])
