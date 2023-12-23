def list_to_string(array):
    return ", ".join(f"'{item}'" if isinstance(item, str) else str(item) for item in array)
