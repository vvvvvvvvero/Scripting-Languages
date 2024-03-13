from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QWidget, \
    QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt6.QtCore import Qt
import mysql.connector
from collections import Counter

CONFIG_DIC = {
    'user': 'root',
    'password': '28ver11ka2002',
    'host': 'localhost',
    'database': 'bike_rentals'
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Bike Rental Statistics')
        self.setFixedSize(700, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        self.label = QLabel('Stations to choose:')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Futura", 24, QFont.Weight.Bold))

        self.left_layout.addWidget(self.label)

        self.combobox = QComboBox(self)
        self.combobox.setFixedSize(300, 30)

        self.left_layout.addWidget(self.combobox)

        self.button = QPushButton('Statistics', self)
        self.button.setFixedSize(300, 30)
        self.button.setStyleSheet("background-color: #505168; color: white; border-radius: 5px;")
        self.button.setFont(QFont("Futura", 16, QFont.Weight.Bold))
        self.button.clicked.connect(self.calculate_statistics)

        self.left_layout.addWidget(self.button)

        self.average_s_label = QLabel("Average duration of journey starting: ")
        self.average_s_label.setFont(QFont("Futura", 16))
        self.right_layout.addWidget(self.average_s_label)
        self.average_s_details = QLineEdit()
        self.average_s_details.setFixedSize(300, 30)
        self.average_s_details.setStyleSheet("border-radius: 5px;")
        self.average_s_details.setReadOnly(True)
        self.right_layout.addWidget(self.average_s_details)

        self.average_e_label = QLabel("Average duration of journey ending: ")
        self.average_e_label.setFont(QFont("Futura", 16))
        self.right_layout.addWidget(self.average_e_label)
        self.average_e_details = QLineEdit()
        self.average_e_details.setFixedSize(300, 30)
        self.average_e_details.setStyleSheet("border-radius: 5px;")
        self.average_e_details.setReadOnly(True)
        self.right_layout.addWidget(self.average_e_details)

        self.bike_count_label = QLabel("Number of different bicycles: ")
        self.bike_count_label.setFont(QFont("Futura", 16))
        self.right_layout.addWidget(self.bike_count_label)
        self.bike_count_details = QLineEdit()
        self.bike_count_details.setFixedSize(300, 30)
        self.bike_count_details.setStyleSheet("border-radius: 5px;")
        self.bike_count_details.setReadOnly(True)
        self.right_layout.addWidget(self.bike_count_details)

        self.most_freq_bike_label = QLabel("Most frequent bicycle: ")
        self.most_freq_bike_label.setFont(QFont("Futura", 16))
        self.right_layout.addWidget(self.most_freq_bike_label)
        self.most_freq_bike_details = QLineEdit()
        self.most_freq_bike_details.setFixedSize(300, 30)
        self.most_freq_bike_details.setStyleSheet("border-radius: 5px;")
        self.most_freq_bike_details.setReadOnly(True)
        self.right_layout.addWidget(self.most_freq_bike_details)

        self.show()

        self.load_stations()

    def load_stations(self):
        connection = mysql.connector.connect(**CONFIG_DIC)
        cursor = connection.cursor()

        try:
            cursor.execute('SELECT station_name FROM Stations')
            stations = cursor.fetchall()

            for station in stations:
                self.combobox.addItem(station[0])

        except mysql.connector.Error as error:
            print('Error: {}'.format(error))
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def calculate_avg_start(selected_station, cursor):
        query = 'SELECT AVG(TIMESTAMPDIFF(MINUTE, R.start_time, R.end_time)) ' \
                'FROM Rentals R INNER JOIN Stations S ON R.rental_station = S.station_id ' \
                'WHERE S.station_name = %s'

        cursor.execute(query, (selected_station,))
        avg_start_duration = cursor.fetchone()[0]
        return avg_start_duration

    @staticmethod
    def calculate_avg_end(selected_station, cursor):
        query = 'SELECT AVG(TIMESTAMPDIFF(MINUTE, R.start_time, R.end_time)) ' \
                'FROM Rentals R INNER JOIN Stations S ON R.return_station = S.station_id ' \
                'WHERE S.station_name = %s'
        cursor.execute(query, (selected_station,))
        avg_end_duration = cursor.fetchone()[0]
        return avg_end_duration

    @staticmethod
    def calculate_bike_count(selected_station, cursor):
        query = 'SELECT COUNT(DISTINCT bike_number) ' \
                'FROM Rentals R INNER JOIN Stations S ' \
                'ON (R.rental_station = S.station_id OR R.return_station = S.station_id) ' \
                'WHERE S.station_name = %s'
        cursor.execute(query, (selected_station,))
        bike_count = cursor.fetchone()[0]
        return bike_count

    @staticmethod
    def calculate_most_freq_bike(selected_station, cursor):
        query = 'SELECT bike_number ' \
                'FROM Rentals INNER JOIN Stations S ' \
                'ON (Rentals.rental_station = S.station_id OR Rentals.return_station = S.station_id) ' \
                'WHERE S.station_name = %s'

        cursor.execute(query, (selected_station,))
        bike_numbers = [row[0] for row in cursor.fetchall()]
        count = Counter(bike_numbers)
        most_freq_bike = count.most_common(1)[0][0]
        return most_freq_bike

    def calculate_statistics(self):
        selected_station = self.combobox.currentText()
        print(selected_station)

        connection = mysql.connector.connect(**CONFIG_DIC)
        cursor = connection.cursor()

        try:
            avg_start_duration = self.calculate_avg_start(selected_station, cursor)
            self.average_s_details.setText(str(avg_start_duration))

            avg_end_duration = self.calculate_avg_end(selected_station, cursor)
            self.average_e_details.setText(str(avg_end_duration))

            bike_count = self.calculate_bike_count(selected_station, cursor)
            self.bike_count_details.setText(str(bike_count))

            most_freq_bike = self.calculate_most_freq_bike(selected_station, cursor)
            self.most_freq_bike_details.setText(str(most_freq_bike))

        except mysql.connector.Error as error:
            print('Error: {}'.format(error))
        finally:
            cursor.close()
            connection.close()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec()
