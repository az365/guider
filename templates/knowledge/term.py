from enum import Enum
from typing import Optional, Iterable, Union
from collections import OrderedDict

from templates.entity import Entity

Term = Entity
Terms = Union[Term, list, None]

class SimpleTerm(Term):
    def __init__(
            self,
            short_name: str,
            synonymes: list,
            definition: str='',

            parent: Terms = None,
            child: Terms = None,

            uses: Terms = None,
            usage: Terms = None,
    ):
        super().__init__(short_name, synonymes=synonymes, definition=definition)

        self.parent = parent
        self.child = child

        self.uses = uses
        self.usage = usage


class LinkType(Enum):
    Parent = 'parent'
    Child = 'child'
    Class = 'class'
    Instance = 'instance'
    Container = 'container'
    Content = 'content'
    Uses = 'uses'
    Usage = 'usage'


link_type_symmetry = (
    (LinkType.Parent, LinkType.Child),
    (LinkType.Class, LinkType.Instance),
    (LinkType.Container, LinkType.Content),
    (LinkType.Uses, LinkType.Usage),
)

def get_inverted_link_type(link_type: LinkType, skip_missing: bool = False) -> Optional[LinkType]:
    for a, b in link_type_symmetry:
        if a == link_type:
            return b
        if b == link_type:
            return a
    if not skip_missing:
        raise ValueError(f'there are no inverted pair for {link_type}')


class LinkedTerm(Term):
    def __init__(
            self,
            short_name: str, synonymes: list, definition: str='',
            parent: Terms = None, child: Terms = None,
            cls: Terms = None, instance: Terms = None,
            container: Terms = None, content: Terms = None,
            uses: Terms = None, usage: Terms = None,
    ):
        super().__init__(short_name, synonymes=synonymes, definition=definition)
        self._links = OrderedDict()
        self.set_linked_terms(LinkType.Parent, parent)
        self.set_linked_terms(LinkType.Child, child)
        self.set_linked_terms(LinkType.Class, cls)
        self.set_linked_terms(LinkType.Instance, instance)
        self.set_linked_terms(LinkType.Container, container)
        self.set_linked_terms(LinkType.Content, content)
        self.set_linked_terms(LinkType.Uses, uses)
        self.set_linked_terms(LinkType.Usage, usage)

    def get_linked_terms(self, link_type: LinkType) -> list:
        return self._links[link_type]

    def set_linked_terms(self, link_type: LinkType, links: Optional[Iterable]=None, symmetrically: bool = True):
        self.clear_linked_terms(link_type, symmetrically=symmetrically)
        if links:
            if isinstance(links, Term):
                links = [links]
            for i in links:
                self.add_linked_term(link_type, i, symmetrically=symmetrically)

    def clear_linked_terms(self, link_type: LinkType, symmetrically: bool = True):
        if symmetrically and link_type in self._links:
            terms = self._links[link_type]
            for i in terms:
                self.drop_linked_term(link_type, i, symmetrically=symmetrically)
        else:
            self._links[link_type] = list()

    def add_linked_term(self, link_type: LinkType, term: Term, symmetrically: bool = True):
        if symmetrically:
            inverted_type = get_inverted_link_type(link_type)
            assert isinstance(term, LinkedTerm)
            term.add_linked_term(inverted_type, self, symmetrically=False)
        terms = self._links[link_type]
        assert isinstance(terms, list)
        terms.append(term)

    def drop_linked_term(self, link_type: LinkType, term: Term, symmetrically: bool = True):
        if symmetrically:
            inverted_type = get_inverted_link_type(link_type)
            assert isinstance(term, LinkedTerm)
            term.drop_linked_term(inverted_type, self, symmetrically=False)
        terms = self._links[link_type]
        assert isinstance(terms, list)
        terms.remove(term)

    def get_props(self) -> OrderedDict:
        props = OrderedDict()
        props['short_name'] = self.short_name
        props['synonymes'] = self.synonymes
        props['definition'] = self.definition
        for k, v in self._links.items():
            assert isinstance(k, LinkType)
            props[k.value] = v
        return props

    def __repr__(self):
        return self.short_name

    def __str__(self):
        if self.synonymes:
            return self.synonymes[0]
        else:
            return self.short_name
