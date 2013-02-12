from five import grok

from uqmc.types.content.kit import UQMCContainer


class UQMCGear(UQMCContainer):
    def get_gear(self):
        return self

    @property
    def count(self):
        return self.total
