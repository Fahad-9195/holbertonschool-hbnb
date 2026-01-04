def require_str(value, field_name: str, min_len: int = 1, max_len: int = 255):
    if value is None:
        raise ValueError(f"{field_name} is required")
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    value = value.strip()
    if len(value) < min_len:
        raise ValueError(f"{field_name} must be at least {min_len} characters")
    if len(value) > max_len:
        raise ValueError(f"{field_name} must be at most {max_len} characters")
    return value

def require_float(value, field_name: str, min_v=None, max_v=None):
    if value is None:
        raise ValueError(f"{field_name} is required")
    try:
        v = float(value)
    except Exception:
        raise ValueError(f"{field_name} must be a number")
    if min_v is not None and v < min_v:
        raise ValueError(f"{field_name} must be >= {min_v}")
    if max_v is not None and v > max_v:
        raise ValueError(f"{field_name} must be <= {max_v}")
    return v

def require_int(value, field_name: str, min_v=None, max_v=None):
    if value is None:
        raise ValueError(f"{field_name} is required")
    try:
        v = int(value)
    except Exception:
        raise ValueError(f"{field_name} must be an integer")
    if min_v is not None and v < min_v:
        raise ValueError(f"{field_name} must be >= {min_v}")
    if max_v is not None and v > max_v:
        raise ValueError(f"{field_name} must be <= {max_v}")
    return v

def require_uuid_str(value, field_name: str):
    # we only validate it's a non-empty string here (UUID format can be enforced later)
    return require_str(value, field_name, min_len=1, max_len=64)
