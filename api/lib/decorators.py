import json
import os.path
import pickle
from functools import wraps

from .json_handler import JSONEncoder


def _io():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            file_path = f"./TmpFiles/{func.__name__}.json"
            data = {'inputs': {'args': args, 'kwargs': kwargs}, 'output': func(*args, **kwargs)}
            if os.path.exists("./TmpFiles"):
                json.dump(data, open(file_path, 'w'), indent=4, cls=JSONEncoder)

            return data['output']
        return wrapper
    return decorator


if __name__ == '__main__':
    @_io()
    def add(a, b):
        return a + b

    # Call the function
    result = add(3, 5)
