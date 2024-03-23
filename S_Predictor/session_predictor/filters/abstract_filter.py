class AbstractFilter:
    def __init__(self, field):
        self.field = field

    def FilterInit(self,storage ="FiltersData.xml"):
        pass

    def FilterApply(self,value,storage ="FiltersData.xml"):
        pass