from .events import Event


def event(*args, **kwargs):
    def generate(f):
        e = Event(f, *args, **kwargs)
        return e
    return generate
