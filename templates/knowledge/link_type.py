from enum import Enum
from typing import Optional


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
