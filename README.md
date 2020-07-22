# cavalcade
*Cavalcade* is a **lightweight, asynchronous event library for Python**. 
The main method for adding *events* is primarily via function decorators, 
although using Event objects is also perfectly legal.

Events are managed by an *event manager* that runs in the background, and as 
events are called or created, they are added to a queue to be processed.

## Features
 * Support for **synchronous and asynchronous events**
 * A builtin **event manager** for queuing and processing events that runs in the background.
 * Support for **decorating functions/methods** as events
 * Support for **explicit event classes**
 * Support for manager **singletons**
 * Support for **callbacks** on completion of event

## Basic Usage
```python
import cavalcade

manager = cavalcade.DefaultManager()
manager.start()  # Start the default manager, it runs in the background

@cavalcade.event()  # Define your event
def event_print(*args, **kwargs):
    print(*args, **kwargs)

event_print('Hello World')  # Run your event
manager.stop()
```

## Common class and decorators
  * **`cavalcade.DefaultManager`:** The default manager to use if you require
  the bare minimum of functionality. Also `cavalcade.managers.DefaultManager`
  * **`cavalcade.Manager`:** The manager base class. You shouldn't use using this
  directly as it's not a *singleton*, The *DefaultManager* is the preferred
  reference implementation of this class. This class's purpose is to be subclassed. Also
  `cavalcade.managers.Manager`
  * **`cavalcade.event`:** The event decorator, to be used when decorating
  functions or methods. Also `cavalcade.decorators.event`.
  * **`cavalcade.Event`:** The base event object. Using the event decorator as
  above returns an object of this type. You can also subclass or instantiate
  this class directly. Also `cavalcade.events.Event`.

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
class VerboseManager(cavalcade.Manager):
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


manager = VerboseManager()
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


### Get the output of your event
```python
import cavalcade
cavalcade.DefaultManager().start()


@cavalcade.event(name='get_words')
def get_words(sentence):
    return sentence.split(' ')

words = get_words('Hello World')
words.wait()
print(words.value())
```
