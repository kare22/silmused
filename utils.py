def list_to_string(array):
    if array is None:
        return ''
    return ", ".join(f"'{item}'" if isinstance(item, str) else str(item) for item in array)
