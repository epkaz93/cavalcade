from __future__ import annotations

import asyncio
import inspect
import time

import typing
from typing import (
    Callable,
    Union,
    List,
    Tuple,
    Dict,
    Any
)

from .managers import DefaultManager, Manager


class EventOutput:
    event = None

    def __init__(self, event: Event):
        self.event = event

    def __call__(self, loop: asyncio.BaseEventLoop = None) -> Any:
        if loop is None:
            loop = asyncio.get_event_loop()

        return loop.run_until_complete(self.wait())

    async def wait(self) -> Any:
        while self.event.is_processing() or not self.event.processed():
            await asyncio.sleep(0.2)

        return self.event.raw_output

    def __get__(self):
        if not self.event.processed():
            return self
        else:
            return self.event.raw_output

    def __repr__(self):
        if self.event.is_processing() or not self.event.processed():
            return f'<{self.event.name} ({hex(id(self.event))}) is still pending completion>'

        else:
            return f'<{self.event.name} ({hex(id(self.event))}) output {type(self.value())}>'

    def value(self):
        return self.event.raw_output


class Event:
    func = None
    f_args = None
    f_kwargs = None
    callback = None
    c_args = None
    c_kwargs = None

    manager = DefaultManager()
    name = 'Event'

    def __init__(self, func: Callable, func_args: Union[Tuple, List] = (), func_kwargs: Dict = None,
                 callback: Callable = None, callback_args: Union[Tuple, List] = (), callback_kwargs: Dict = None,
                 manager: Manager = None, name: str = None):

        self.func = func
        self.f_args = func_args
        self.f_kwargs = func_kwargs if func_kwargs else {}

        self.callback = callback
        self.c_args = callback_args
        self.c_kwargs = callback_kwargs if callback_kwargs else {}

        self.manager = manager if manager else self.manager
        self.name = name if name else self.name
        self.output = EventOutput(self)

        self.raw_output = None
        self._is_processing = False
        self._is_processed = False

    def __call__(self, *args, **kwargs) -> EventOutput:
        self.manager.put_nowait((self, args, kwargs))
        return self.output

    async def process(self, *args, **kwargs):
        self._is_processing = True
        kwargs.update(self.f_kwargs)
        args = args + self.f_args
        if inspect.iscoroutine(self.func):
            self.raw_output = await self.func(*args, **kwargs)
        else:
            self.raw_output = self.func(*args, **kwargs)
        self._is_processing = False
        self._is_processed = True

        if self.callback:
            if inspect.iscoroutine(self.callback):
                await self.callback(*self.c_args, **self.c_kwargs)
            else:
                self.callback(*self.c_args, **self.c_kwargs)

    def is_processing(self) -> bool:
        return self._is_processing

    def is_processed(self) -> bool:
        return self._is_processed

    def processing(self) -> bool:
        return self.is_processing()

    def processed(self) -> bool:
        return self.is_processed()

    def wait(self):
        while not self.processed():
            time.sleep(0.2)