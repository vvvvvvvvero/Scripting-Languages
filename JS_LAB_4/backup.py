import os
from utils import get_and_check_dir
from utils import get_backup_dir
import subprocess
from datetime import datetime
import csv


def process_directory():
    dir_path = get_and_check_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dirname = os.path.basename(dir_path)
    backup_file_name = f"{timestamp}_{dirname}.zip"

    backup_dir = get_backup_dir()
    if not os.path.isdir(backup_dir):
        os.makedirs(backup_dir)

    backup_file_path = os.path.join(backup_dir, backup_file_name)

    subprocess.run(["zip", "-r", backup_file_path, dir_path])

    backup_history_file = os.path.join(backup_dir, 'backup_history.csv')
    backup_record = [timestamp, dir_path, backup_file_name]
    field_names = ['date', 'directory', 'filename']

    with open(backup_history_file, 'a') as f:
        csv_writer = csv.writer(f)
        if os.path.exists(backup_history_file):
            csv_writer.writerow(backup_record)
        else:
            csv_writer.writerow(field_names)
            csv_writer.writerow(backup_record)


if __name__ == '__main__':
    process_directory()
