def normalize_string(strr: str):
    normalized_str = strr.strip().replace('\n', '')
    if normalized_str.isalpha():
        return normalized_str
    else:
        raise ValueError("String can only be english alphabet.")
