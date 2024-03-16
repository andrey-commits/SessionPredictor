class AbstractFilter:
    def __init__(self, field):
        self.field = field

    def FilterInit(self):
        pass

    def FilterApply(self,value):
        pass