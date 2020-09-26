from datetime import datetime, timezone, timedelta
from bs4 import NavigableString, Comment

def str_is_set(string):
    return string


def is_string(obj):
    return not isinstance(obj, Comment) and isinstance(obj, NavigableString)


def to_utc(timestamp):
    return timestamp.astimezone(tz=timezone.utc)


def set_ist_zone(timestamp):
    timestamp.replace(tzinfo=timezone(timedelta(hours=5, minutes=30)))


def ist_to_utc(timestamp):
    set_ist_zone(timestamp)
    return to_utc(timestamp)

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