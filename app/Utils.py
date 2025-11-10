import os

def load_file(path, binary=False):
    mode = "rb" if binary else "r"
    try:
        if binary:
            with open(path, mode) as f:   # No encoding for binary
                return f.read()
        else:
            with open(path, mode, encoding="utf-8") as f:
                return f.read()
    except FileNotFoundError:
        return None
