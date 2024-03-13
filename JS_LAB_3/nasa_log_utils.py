def convert_bytes(size: str) -> int:
    if size.isnumeric():
        return int(size)
    else:
        return 0


def get_successful_requests(dict_list):
    success_sum = 0
    for entry in dict_list:
        if entry['code'] == 200:
            success_sum += 1

    return success_sum
