def list_to_string(array):
    if array is None:
        return ''
    return ", ".join(f"'{item}'" if isinstance(item, str) else str(item) for item in array)


def normalize_expected_value(value):
    if value == "NULL" or value == "None":
        return None
    return value


def check_matching_value_types(input_list, input_type):
    for inp in input_list:
        if not isinstance(inp, input_type):
            raise AttributeError(
                f"Expected value {inp} datatype: {type(inp)} doesn't match the required type: {input_type}")


def extract_value_from_tuple(input_list):
    out_list = []
    if input_list is None:
        out_list.append(input_list)
    else:
        for expected in input_list:
            if isinstance(expected, tuple):
                out_list.append(expected[0])
            else:
                out_list.append(expected)
    return out_list


def check_all_results(actual_list, expected_list, allow_extra_values):
    input_list = extract_value_from_tuple(actual_list)
    expected = extract_value_from_tuple(expected_list)

    found = []
    not_found = []
    unexpected_value = []
    assessment = True
    # Actual values found from expected and not expected list
    for actual in input_list:
        if actual in expected:
            found.append(actual)
        elif actual not in expected:
            unexpected_value.append(actual)

    # Expected values missing from actually found values
    for exp in expected:
        if exp not in found:
            not_found.append(exp)

    if allow_extra_values:
        assessment = len(not_found) == 0
        unexpected_value = []
    else:
        assessment = (
                len(not_found) == 0
                and len(unexpected_value) == 0
        )

    return {
        "assessment": assessment,
        "expected_value": not_found,
        "unexpected_value": unexpected_value
    }


# Used mainly for should_exist = False
def find_matching_values(actual_list, expected_list):
    actual_values = extract_value_from_tuple(actual_list)

    found_values = []

    for actual in actual_values:
        if actual in expected_list:
            found_values.append(actual)

    return found_values
