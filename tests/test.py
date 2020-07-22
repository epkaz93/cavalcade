import sys
import cavalcade

manager = cavalcade.DefaultManager()

_exit = exit


def exit():
    manager.stop()
    _exit()


@cavalcade.Event
def test():
    print('test')


# use event object for decoration, not really recommended but perfectly valid still
@cavalcade.Event
def event_print(string):
    print(string)


manager.start()

output = test()

print(output())

event_print('Hello World')


# use event function for decoration, recommended because it allows you to define args (not used here)
@cavalcade.event()
def done():
    print('Event Done')


# use event function for decoration, recommended because it allows you to define args
@cavalcade.event(name='test2', callback=done)
def test2(string):
    print(string)


if not sys.flags.interactive:
    exit()
