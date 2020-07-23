from __future__ import annotations

from ..events import Event

import typing
from typing import (
    Callable,
    Union,
    Tuple,
    List,
    Dict

)

if typing.TYPE_CHECKING:
    from .graph import Graph


class Node(Event):
    graph = None
    inputs = None
    outputs = None

    def __init__(self, func: Callable, graph: Graph = None,
                 input_args: Union[Tuple, List] = (), input_kwargs: Dict = None,
                 *args, **kwargs):
        super().__init__(func, *args, **kwargs)

        self.graph = graph if graph else self.graph
        if self.graph is None:
            raise ValueError('graph cannot be "None"')

        # replicate if func in event
        if issubclass(type(func), Event) and not issubclass(type(func), Node):
            for attr in dir(func):
                setattr(self, attr, getattr(func, attr))

        self.input_args = input_args
        self.input_kwargs = input_kwargs if input_kwargs else {}

        self.input_nodes = []
        for arg in self.input_args:
            if not issubclass(type(arg), Node):
                if callable(arg):
                    n = Node(arg)
                else:
                    n = arg
            else:
                n = Node(func=lambda: arg)
            self.input_nodes.append(n)

            if n not in self.graph.nodes:
                self.graph.add_node(n)

        self.graph