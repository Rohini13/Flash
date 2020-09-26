from datetime import datetime, timezone, timedelta
from bs4 import NavigableString, Comment

def remove_duplicates(objects, key, prefer=None):
    unique_set = set()

    def is_unique(obj):
        if obj[key] not in unique_set:
            unique_set.add(obj[key])
            return True
        return False

    if prefer is None:
        return list(filter(is_unique, objects))

    preferred = {}
    for obj in objects:
        prkey = obj[key]
        if preferred.get(prkey) is None:
            preferred[prkey] = obj
            continue
        if not preferred[prkey][prefer]:
            preferred[prkey] = obj

    return list(preferred.values())