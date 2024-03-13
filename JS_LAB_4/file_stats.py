import sys
from collections import Counter


def get_stats_in_tsv():
    file_path = sys.stdin.readline().strip()

    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
    except FileNotFoundError:
        print("File not found")
        sys.exit(1)

    path = file_path
    num_of_chars = len(file_content)
    num_of_words = len(file_content.split())
    num_of_lines = len(file_content.splitlines())
    the_most_freq_char = Counter(file_content).most_common(1)[0][0]
    quantity_char = Counter(file_content).most_common(1)[0][1]
    the_most_freq_word = Counter(file_content.split()).most_common(1)[0][0]
    quantity_word = Counter(file_content.split()).most_common(1)[0][1]

    print("Path\tChars_num\tWords_num\tLines_num\tFreq_char\tQuantity\tFreq_word\tQuantity")
    print(f"{path}\t{num_of_chars}\t{num_of_words}\t{num_of_lines}\t{the_most_freq_char}\t{quantity_char}"
          f"\t{the_most_freq_word}\t{quantity_word}")


if __name__ == "__main__":
    get_stats_in_tsv()
