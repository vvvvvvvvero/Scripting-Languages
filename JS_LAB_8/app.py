import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, \
    QFileDialog, QListWidget, QLabel, QListWidgetItem, QDateTimeEdit
from PyQt6.QtCore import QStandardPaths, Qt, QDateTime

from process_logs import LogUtils, LOG_TIMESTAMP, LOG_HOST, LOG_ID, LOG_MESSAGE, USER, IP
from PyQt6.QtGui import QFontDatabase, QFont


class LogBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.log_utils = LogUtils()

        self.setWindowTitle("SSH Server Logs Browser")
        self.setFixedSize(800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        self.top_layout = QHBoxLayout()

        self.load_button = QPushButton("Load")
        self.load_button.setFixedSize(80, 30)
        self.load_button.setStyleSheet("background-color: #505168; color: white; border-radius: 5px;")
        self.load_button.setFont(QFont("Futura", 16, QFont.Weight.Bold))
        self.load_button.clicked.connect(self.load_file)
        self.top_layout.addWidget(self.load_button)

        self.file_path_input = QLineEdit()
        self.file_path_input.setFixedSize(650, 30)
        self.file_path_input.setStyleSheet("border-radius: 5px;")
        self.file_path_input.setReadOnly(True)
        self.top_layout.addWidget(self.file_path_input)

        self.main_layout.addLayout(self.top_layout)

        self.central_layout = QHBoxLayout()
        self.main_layout.addLayout(self.central_layout)

        self.left_layout = QVBoxLayout()
        self.central_layout.addLayout(self.left_layout)

        self.filter_layout = QHBoxLayout()

        self.start_datetime = QDateTimeEdit()
        self.start_datetime.setDisplayFormat("MMM dd hh:mm:ss")
        self.start_datetime.setFont(QFont("Futura", 14))
        self.start_datetime.setFixedSize(200, 30)
        self.start_datetime.setDateTime(QDateTime.currentDateTime())
        self.filter_layout.addWidget(self.start_datetime)

        self.end_datetime = QDateTimeEdit()
        self.end_datetime.setDisplayFormat("MMM dd hh:mm:ss")
        self.end_datetime.setFont(QFont("Futura", 14))
        self.end_datetime.setFixedSize(200, 30)
        self.end_datetime.setDateTime(QDateTime.currentDateTime())
        self.filter_layout.addWidget(self.end_datetime)

        self.left_layout.addLayout(self.filter_layout)

        self.filter_button_layout = QHBoxLayout()
        self.left_layout.addLayout(self.filter_button_layout)

        self.filter_button = QPushButton("Filter")
        self.filter_button.setFont(QFont("Futura", 18))
        self.filter_button.setFixedSize(180, 30)
        self.filter_button.setStyleSheet("background-color: #27233A; color: white; border-radius: 5px;")
        self.filter_button.clicked.connect(self.filter_logs)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setFont(QFont("Futura", 18))
        self.reset_button.setFixedSize(180, 30)
        self.reset_button.setStyleSheet("background-color: #27233A; color: white; border-radius: 5px;")
        self.reset_button.clicked.connect(self.reset_logs)

        self.filter_button_layout.addWidget(self.filter_button)
        self.filter_button_layout.addWidget(self.reset_button)

        self.log_list = QListWidget()
        self.log_list.itemSelectionChanged.connect(self.show_log_properties)
        self.left_layout.addWidget(self.log_list)

        self.right_layout = QVBoxLayout()
        self.central_layout.addLayout(self.right_layout)

        self.log_details_label = QLabel("Selected log details")
        self.log_details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.log_details_label.setFont(QFont("Futura", 24, QFont.Weight.Bold))
        self.right_layout.addWidget(self.log_details_label)

        self.timestamp_label = QLabel("Timestamp:")
        self.timestamp_label.setFont(QFont("Futura", 16))
        self.right_layout.addWidget(self.timestamp_label)
        self.timestamp_details = QLineEdit()
        self.timestamp_details.setFixedSize(300, 30)
        self.timestamp_details.setStyleSheet("border-radius: 5px;")
        self.timestamp_details.setReadOnly(True)
        self.right_layout.addWidget(self.timestamp_details)

        self.host_label = QLabel("Host name:")
        self.host_label.setFont(QFont("Futura", 16))
        self.right_layout.addWidget(self.host_label)
        self.host_details = QLineEdit()
        self.host_details.setFixedSize(300, 30)
        self.host_details.setStyleSheet("border-radius: 5px;")
        self.host_details.setReadOnly(True)
        self.right_layout.addWidget(self.host_details)

        self.id_label = QLabel("Process ID:")
        self.id_label.setFont(QFont("Futura", 16))
        self.right_layout.addWidget(self.id_label)
        self.id_details = QLineEdit()
        self.id_details.setFixedSize(300, 30)
        self.id_details.setStyleSheet("border-radius: 5px;")
        self.id_details.setReadOnly(True)
        self.right_layout.addWidget(self.id_details)

        self.ip_label = QLabel("IP Address:")
        self.ip_label.setFont(QFont("Futura", 16))
        self.right_layout.addWidget(self.ip_label)
        self.ip_details = QLineEdit()
        self.ip_details.setFixedSize(300, 30)
        self.ip_details.setStyleSheet("border-radius: 5px;")
        self.ip_details.setReadOnly(True)
        self.right_layout.addWidget(self.ip_details)

        self.user_label = QLabel("User name:")
        self.user_label.setFont(QFont("Futura", 16))
        self.right_layout.addWidget(self.user_label)
        self.user_details = QLineEdit()
        self.user_details.setFixedSize(300, 30)
        self.user_details.setStyleSheet("border-radius: 5px;")
        self.user_details.setReadOnly(True)
        self.right_layout.addWidget(self.user_details)

        self.message_layout = QVBoxLayout()
        self.main_layout.addLayout(self.message_layout)

        self.message_label = QLabel("Message:")
        self.message_label.setFont(QFont("Futura", 20))
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_layout.addWidget(self.message_label)
        self.message_details = QLineEdit()
        self.message_details.setFixedSize(780, 30)
        self.message_details.setStyleSheet("border-radius: 5px;")
        self.message_details.setReadOnly(True)
        self.message_layout.addWidget(self.message_details)

        self.bottom_layout = QHBoxLayout()
        self.main_layout.addLayout(self.bottom_layout)

        self.previous_button = QPushButton("Previous")
        self.previous_button.setFixedSize(150, 40)
        self.previous_button.setStyleSheet("background-color: #505168; color: white; border-radius: 10px;")
        self.previous_button.setFont(QFont("Futura", 22, QFont.Weight.Bold))
        self.previous_button.clicked.connect(self.previous_log)
        self.bottom_layout.addWidget(self.previous_button)

        self.next_button = QPushButton("Next")
        self.next_button.setFixedSize(150, 40)
        self.next_button.setStyleSheet("background-color: #505168; color: white; border-radius: 10px;")
        self.next_button.setFont(QFont("Futura", 22, QFont.Weight.Bold))
        self.next_button.clicked.connect(self.next_log)
        self.bottom_layout.addWidget(self.next_button)

        self.list_of_all_logs = []

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Log File", QStandardPaths.
                                                   writableLocation(QStandardPaths.StandardLocation.
                                                                    HomeLocation), "Log Files (*.log)")
        if file_path:
            logs = self.log_utils.load_log_file(file_path)
            self.file_path_input.setText(file_path)
            self.list_of_all_logs = logs
            self.update_log_list(logs)

    def filter_logs(self):
        start_datetime = self.start_datetime.dateTime().toString("MMM dd hh:mm:ss")
        end_datetime = self.end_datetime.dateTime().toString("MMM dd hh:mm:ss")
        filtered_logs = self.log_utils.filter_logs(self.list_of_all_logs, start_datetime, end_datetime)
        self.update_log_list(filtered_logs)

    def update_log_list(self, logs):
        self.log_list.clear()
        for log in logs:
            short_log = log[:70] + "..." if len(log) > 70 else log
            log_item = QListWidgetItem(short_log)
            log_item.full_log = log
            self.log_list.addItem(log_item)

    def reset_logs(self):
        self.update_log_list(self.list_of_all_logs)

    def show_log_properties(self):
        selected = self.log_list.selectedItems()
        if selected:
            selected_log = selected[0].full_log
            log_properties = self.log_utils.parse_log(selected_log)
            self.timestamp_details.setText(log_properties[LOG_TIMESTAMP])
            self.host_details.setText(log_properties[LOG_HOST])
            self.id_details.setText(log_properties[LOG_ID])
            self.message_details.setText(log_properties[LOG_MESSAGE])
            self.ip_details.setText(log_properties[IP])
            self.user_details.setText(log_properties[USER])

    def next_log(self):
        selected = self.log_list.selectedItems()
        if selected:
            current_index = self.log_list.row(selected[0])
            if current_index < self.log_list.count() - 1:
                self.log_list.setCurrentRow(current_index + 1)

    def previous_log(self):
        selected = self.log_list.selectedItems()
        if selected:
            current_index = self.log_list.row(selected[0])
            if current_index > 0:
                self.log_list.setCurrentRow(current_index - 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogBrowser()
    window.show()
    sys.exit(app.exec())
