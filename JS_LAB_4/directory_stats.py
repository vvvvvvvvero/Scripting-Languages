import subprocess
import sys
import os
import csv
from utils import get_and_check_dir

file_stats_path = "/Users/veraemelianova/PycharmProjects/JS_LAB_4/file_stats.py"


def process_file(file_path):
    tsv_output = subprocess.run([sys.executable, file_stats_path], capture_output=True, input=file_path, text=True)
    path, chars_num, words_num, lines_num, freq_char, quant_char, freq_word, quant_word \
        = tsv_output.stdout.splitlines()[1].split("\t")
    file_stats_dict = {
        "Path": path,
        "Chars_num": int(chars_num),
        "Words_num": int(words_num),
        "Lines_num": int(lines_num),
        "Most_freq_char": (str(freq_char), int(quant_char)),
        "Most_freq_word": (str(freq_word), int(quant_word))
    }
    return file_stats_dict


def process_directory(dir_path):
    dict_list = []

    for file in os.listdir(dir_path):
        if file.endswith(".txt"):
            file_path = os.path.join(dir_path, file)
            dict_list.append(process_file(file_path))
    return dict_list


def get_stats():
    directory_path = get_and_check_dir()

    stats_dictionaries = process_directory(directory_path)

    num_of_processed_files = len(stats_dictionaries)
    num_of_chars = sum([d["Chars_num"] for d in stats_dictionaries])
    num_of_words = sum([d["Words_num"] for d in stats_dictionaries])
    num_of_lines = sum([d["Lines_num"] for d in stats_dictionaries])
    most_frequent_char = sorted(list(d["Most_freq_char"] for d in stats_dictionaries),
                                key=lambda x: x[1], reverse=True)[0]
    most_frequent_word = sorted(list(d["Most_freq_word"] for d in stats_dictionaries),
                                key=lambda x: x[1], reverse=True)[0]

    field_names = ["PROCESSED FILES", "CHARS", "WORDS", "LINES", "MOST FREQUENT CHAR", "MOST FREQUENT WORD"]
    values = [num_of_processed_files, num_of_chars, num_of_words, num_of_lines, most_frequent_char, most_frequent_word]

    csv_writer = csv.writer(sys.stdout)
    csv_writer.writerow(field_names)
    csv_writer.writerow(values)


if __name__ == '__main__':
    get_stats()
