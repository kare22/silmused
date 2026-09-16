def list_to_string(array):
    if array is None:
        return ''
    return ", ".join(f"'{item}'" if isinstance(item, str) else str(item) for item in array)


def check_all_results(result_list, expected_list):
    input_list = {input for input, in result_list}
    not_found = []
    for expected_value in expected_list:
        if expected_value not in input_list:
            not_found.append(expected_value)

    if len(not_found) > 0:
        return False, not_found
    return True, not_found
