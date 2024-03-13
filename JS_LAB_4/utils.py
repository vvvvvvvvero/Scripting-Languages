import os
import sys
from os import environ


def get_and_check_dir():
    if len(sys.argv) != 2:
        print("python3 directory_stats.py directory_path")
        sys.exit(1)

    dir_path = sys.argv[1]

    if not os.path.isdir(dir_path):
        print("Directory not found")
        sys.exit(1)
    return dir_path


def get_backup_dir():
    backup_dir = os.environ.get('BACKUPS_DIR')
    if backup_dir is None:
        home_dir = environ.get("HOME")
        backup_dir = os.path.join(home_dir, ".backups")
    return backup_dir
