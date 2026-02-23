from typing import Union

from templates.entity import Entity

Term = Entity
Terms = Union[Term, list, None]


class SimpleTerm(Term):
    def __init__(
            self,
            tech_name: str,
            synonymes: list,
            definition: str = '',

            parent: Terms = None,
            child: Terms = None,

            uses: Terms = None,
            usage: Terms = None,
    ):
        super().__init__(tech_name, synonymes=synonymes, definition=definition)

        self.parent = parent
        self.child = child

        self.uses = uses
        self.usage = usage
