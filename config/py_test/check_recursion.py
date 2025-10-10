from typing import get_args, get_origin
import dataclasses


def check_recursion(cls, seen=None, path=""):
    if seen is None:
        seen = set()
    if cls in seen:
        print(f"❗ Recursive reference detected: {path} -> {cls}")
        return
    seen.add(cls)

    if not dataclasses.is_dataclass(cls):
        return

    for field in dataclasses.fields(cls):
        ftype = field.type
        args = get_args(ftype)
        origin = get_origin(ftype)
        if args:
            for arg in args:
                check_recursion(arg, seen.copy(), f"{path}.{field.name}")
        elif isinstance(ftype, type):
            check_recursion(ftype, seen.copy(), f"{path}.{field.name}")


from lerobot.common.teleoperators.lekiwi_leader import LekiwiLeaderConfig

check_recursion(LekiwiLeaderConfig)
