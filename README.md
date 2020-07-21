# cavalcade
## Basic Usage
```python
import cavalcade

manager = cavalcade.DefaultManager()
manager.start()  # Start the default manager

@cavalcade.event()  # Define your event
def event_print(*args, **kwargs):
    print(*args, **kwargs)

event_print('Hello World')  # Run your event
```


# Examples

## Manager Examples
### Start Manager
```python
import cavalcade

manager = cavalcade.DefaultManager()
manager.start()
```

### Custom Manager
```python
import cavalcade
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


# It is not technically required to make your manager a singleton
# But it is good practice
@cavalcade.Singleton
class NoisyManager(cavalcade.Manager):
    def __init__(self):
        super().__init__()
        logger.info(f'{self.__class__.__name__}: Created')

    def start(self):
        logger.info(f'{self.__class__.__name__}: Starting')
        super().start()
        logger.info(f'{self.__class__.__name__}: Started')

    def process_event(self, event, args, kwargs):
        logging.info(f'{self.__class__.__name__}: Processing Event {event.name}')
        super().process_event(event, args, kwargs)


manager = NoisyManager()
manager.start()
```

## Event Examples

### Decorate a function/method as an event
```python
import cavalcade

manager = cavalcade.DefaultManager()
manager.start()

@cavalcade.event()
def event_print(string):
    print(string)

# now whenever you call event_print it uses the event queue

event_print('Hello World')
```

### Using async functions/methods
```python
import cavalcade
import asyncio

@cavalcade.event(name='Delayed_Print')
async def delayed_print(string, delay):
    await asyncio.sleep(delay)
    print(string)
```

### Add a callback
```python
import cavalcade
import asyncio

# I'm going to use another event as my callback, which is good practice
# That being said, there is no technical restriction to use an event

@cavalcade.event(name='Done')
def done(event: cavalcade.Event):
    print(f'Event {event.name} Done')


@cavalcade.event(name='Delayed_Print', callback=lambda: done(delayed_print))
async def delayed_print(string: str, delay: int):
    await asyncio.sleep(delay)
    print(string)
```
