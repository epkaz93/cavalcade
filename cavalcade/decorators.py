from .events import Event
from .graphs import Node


def event(*args, **kwargs):
    def generate(f):
        e = Event(f, *args, **kwargs)
        return e
    return generate


def node(*args, **kwargs):
    def generate(f):
        e = Node(f, *args, **kwargs)
        return e
    return generate
