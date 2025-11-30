from typing import Optional, Iterable, Iterator
from collections import OrderedDict

from templates.knowledge.simple_term import Term, Terms
from templates.knowledge.link_type import LinkType, get_inverted_link_type


class LinkedTerm(Term):
    def __init__(
            self,
            short_name: str,
            synonymes: Optional[list] = None,
            definition: str = '',

            parent: Terms = None, child: Terms = None,
            cls: Terms = None, instance: Terms = None,
            container: Terms = None, content: Terms = None,
            uses: Terms = None, usage: Terms = None,
    ):
        super().__init__(short_name, synonymes=synonymes or list(), definition=definition)
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
        if isinstance(term, str):
            found_term = self.get_term_by_id(term)
            if not found_term:
                term = LinkedTerm(term)
        if symmetrically:
            inverted_type = get_inverted_link_type(link_type)
            assert isinstance(term, LinkedTerm), TypeError(f'{term} is {type(term)}, not LinkedTerm')
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

    def get_linked_terms_iterator(self, recursively: bool = False, ignore_names: Optional[set] = None) -> Iterator[Term]:
        if recursively:
            if ignore_names is None:
                ignore_names = set()
            for term in self.get_linked_terms_iterator():
                if isinstance(term, LinkedTerm):
                    name = term.short_name
                else:
                    raise TypeError(f'{term} is {type(term)}, not LinkedTerm')
                if name not in ignore_names:
                    yield term
                    ignore_names.add(name)
                    yield from term.get_linked_terms_iterator(recursively=True, ignore_names=ignore_names)
        else:
            for linked_terms in self._links.values():
                for term in linked_terms:
                    yield term

    def get_term_by_id(self, short_name: str, recursively: bool = False, ignore_names: Optional[set] = None):
        for i in self.get_linked_terms_iterator(recursively=recursively, ignore_names=ignore_names):
            if i.short_name == short_name:
                return i

    def get_term_by_name(self, name: str, recursively: bool = False, ignore_names: Optional[set] = None):
        for i in self.get_linked_terms_iterator(recursively=recursively, ignore_names=ignore_names):
            names = [i.short_name] + i.synonymes
            if name in names:
                return i

    def get_repr(self):
        return self.short_name

    def __repr__(self):
        return self.get_repr()

    def __str__(self):
        if self.synonymes:
            return self.synonymes[0]
        else:
            return self.short_name
