import sys
import os
import csv
import subprocess
from utils import get_backup_dir


def get_backup_list():
    backup_dir = get_backup_dir()
    csv_history_file = os.path.join(backup_dir, 'backup_history.csv')

    backup_list = []
    if os.path.exists(csv_history_file):
        with open(csv_history_file, 'r') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                backup_list.append(row)

    backup_list.reverse()
    return backup_list


def list_backups():
    backup_list = get_backup_list()
    if not backup_list:
        print('Cant find backup history.')
        return
    print('Backup history:')
    for i, backup in enumerate(backup_list):
        print(f'{i+1}. {backup[0]} - {backup[1]} - {backup[2]}')


def select_backup(backup_index):
    backup_list = get_backup_list()
    if backup_index < 1 or backup_index > len(backup_list):
        print('Invalid backup index.')
        return
    return backup_list[backup_index - 1]


def restore_backup(backup_to_restore, target_directory):

    backup_dir = get_backup_dir()
    backup_file = os.path.join(backup_dir, backup_to_restore[2])

    if os.path.exists(target_directory):
        subprocess.run(['rm', '-rf', target_directory])

    os.makedirs(target_directory)

    subprocess.run(['unzip', backup_file, '-d', target_directory])


def main(target_directory):
    list_backups()
    backup_index = int(input('Select a backup to restore: '))
    backup_to_restore = select_backup(backup_index)
    restore_backup(backup_to_restore, target_directory)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = os.getcwd()

    main(target_dir)



