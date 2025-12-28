from abstract.common_abstract import CommonAbstract

class Entity(CommonAbstract):
    def __init__(self, short_name: str, synonymes: list, definition: str):
        self.short_name = short_name
        self.synonymes = synonymes
        self.definition = definition
