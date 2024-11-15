#!/usr/bin/env python3
from typing import List


def check_path(path: str, excluded: List[str]) -> bool:
    path = path if path.endswith('/') else path + '/'
    for get_path in excluded:
        if get_path.endswith('*'):
            if path.startswith(get_path[:-1]):
                return False
            elif path == get_path:
                return False
    return True


print(check_path("/api/v1/users", ["/api/v1/stat*"]))