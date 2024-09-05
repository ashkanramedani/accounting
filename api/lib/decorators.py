import json
import os.path
import time
from datetime import datetime
from functools import wraps

from lib.json_handler import JSONEncoder


def modify_timer(timer: float):
    factor = 0
    while timer < 0.1:
        timer *= 10
        factor += 1
    return f'{timer:.2f} (*1e{factor})'


def DEV_io(mode: str = "w"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            file_path = f"{func.__name__}.json"

            start = time.time()
            res = func(*args, **kwargs)
            end = time.time()
            data = {'time': modify_timer(end - start), 'inputs': {'args': args, 'kwargs': kwargs}, 'output': res}
            if os.path.exists("DBug_IO"):
                if mode == 'a':
                    OBJ = json.load(open(os.path.join("DBug_IO", file_path)))
                    OBJ[str(datetime.now())] = data
                    json.dump(OBJ, open(os.path.join("DBug_IO", file_path), 'w'), indent=4, cls=JSONEncoder)
                elif mode == 'w':
                    json.dump(data, open(os.path.join("DBug_IO", file_path), 'w'), indent=4, cls=JSONEncoder)
            return data['output']

        return wrapper

    return decorator


if __name__ == '__main__':
    @DEV_io()
    def add(a, b):
        return a + b


    # Call the function
    result = add(3, 5)
