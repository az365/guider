from abstract.common_abstract import CommonAbstract

class Entity(CommonAbstract):
    def __init__(self, tech_name: str, synonymes: list, definition: str):
        self.tech_name = tech_name
        self.synonymes = synonymes
        self.definition = definition
