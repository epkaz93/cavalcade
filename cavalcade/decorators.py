from .events import Event, EventFactory


def event(*args, **kwargs):
    def generate(f):
        e = Event(f, *args, **kwargs)
        return e
    return generate


def event_factory(*args, **kwargs):
    def generate(f):
        e = EventFactory(f, *args, **kwargs)
        return e
    return generate
