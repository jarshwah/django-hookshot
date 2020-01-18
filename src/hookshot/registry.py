import re
import typing as t
from collections import namedtuple

HookArgs = namedtuple("HookArgs", ["name", "func", "insecure", "description"])
_registry: t.Mapping[str, HookArgs] = {}

name_pattern = re.compile(r"^[a-zA-Z][-_a-zA-Z\d]+$")


def webhook(name: str, insecure=False, description: t.Optional[str] = None):
    match = name_pattern.match(name)
    if not match:
        raise ValueError(
            r"webhook name '{}' does not match the pattern '{}'".format(name, name_pattern.pattern)
        )

    def register(func):
        hook_args = HookArgs(name, func, insecure, description)
        _registry[name] = hook_args
        return func

    return register


class RegistryChoices:
    def __iter__(self):
        yield from sorted(zip(list(_registry.keys()), list(_registry.keys())))
