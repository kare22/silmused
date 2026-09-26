def list_to_string(array):
    if array is None:
        return ''
    return ", ".join(f"'{item}'" if isinstance(item, str) else str(item) for item in array)


def extract_value_from_tuple(input_list):
    out_list = []
    for expected in input_list:
        if isinstance(expected, str):
            out_list.append(expected)
        elif isinstance(expected, tuple):
            out_list.append(expected[0])
        else:
            raise AttributeError(f"Expected value is not a string or tuple: {expected}, but type: {type(expected)}")
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
        if len(not_found) > 0:
            assessment = False
        else:
            assessment = True
        unexpected_value = []
    elif not allow_extra_values:
        if len(found) < len(expected) and len(unexpected_value) > 0:
            assessment = False
        elif len(unexpected_value) > 0:
            assessment = False
        elif len(found) < len(expected):
            assessment = False
        else:
            assessment = True

    result = {"assessment": assessment, "expected_value": not_found, "unexpected_value": unexpected_value}
    return result
