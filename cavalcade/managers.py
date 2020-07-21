from __future__ import annotations

import asyncio
from asyncio import Queue
import threading
import traceback
import logging

import typing
if typing.TYPE_CHECKING:
    from .events import Event


class Singleton:
    def __init__(self, class_):
        self.class_ = class_
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.class_(*args, **kwargs)
        return self.instance


class Manager(Queue):
    name = None
    _stopping = False
    thread = None
    loop = None
    raise_ = False

    def __init__(self):
        super().__init__()
        self._task = None
        self.thread = None

    def start(self):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.start_manager, args=(self.loop, ))
        self.thread.start()

    def start_manager(self, loop: asyncio.BaseEventLoop):
        loop.run_until_complete(self.run_manager())

    async def run_manager(self):
        while not self.is_stopping():
            try:
                await self.step()
            except KeyboardInterrupt:
                self.stop()

        while self.qsize():
            await self.step()

    async def step(self):
        if self.qsize():
            event, args, kwargs = self.get_nowait()
            try:
                await self.process_event(event, args, kwargs)
            except:
                if self.raise_:
                    raise
                else:
                    logging.exception(traceback.format_exc())
        else:
            await asyncio.sleep(0.2)

    async def process_event(self, event: Event, args: typing.Union[typing.List, typing.Tuple], kwargs: typing.Dict):
        await event.process(*args, **kwargs)

    def is_stopping(self):
        return self._stopping

    def stop(self):
        self._stopping = True

    def task(self) -> asyncio.Task:
        return self._task

    def is_alive(self):
        if self.thread:
            return self.thread.is_alive()
        else:
            return False


@Singleton
class DefaultManager(Manager):
    pass
