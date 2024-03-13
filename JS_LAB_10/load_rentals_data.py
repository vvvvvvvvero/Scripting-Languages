import sys
import mysql.connector
import csv


def load_data(csv_file, database_name):
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='28ver11ka2002',
        database=database_name)
    cursor = mydb.cursor()

    try:
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)

            sql_select = 'SELECT station_id, station_name FROM Stations'
            cursor.execute(sql_select)
            stations = cursor.fetchall()
            station_dict = {s_name: s_id for s_id, s_name in stations}

            for row in csv_reader:
                rental_id = int(row[0])
                bike_number = int(row[1])
                start_time = row[2]
                end_time = row[3]
                rental_station = station_dict[row[4]]
                return_station = station_dict[row[5]]

                values = (rental_id, bike_number, start_time, end_time, rental_station, return_station)
                sql_insert = 'INSERT INTO Rentals' \
                             ' (rental_id, bike_number, start_time, end_time, rental_station, return_station)' \
                             ' VALUES (%s, %s, %s, %s, %s, %s)'
                cursor.execute(sql_insert, values)

        mydb.commit()
        print('Data inserted successfully.')

    except mysql.connector.Error as err:
        print('Failed creating database: {}'.format(err))
        exit(1)

    finally:
        cursor.close()
        mydb.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 load_rentals_data.py csv_file bike_rentals')
        exit(1)
    else:
        load_data(sys.argv[1], sys.argv[2])
