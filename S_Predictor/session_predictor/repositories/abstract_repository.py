class AbstractRepository:
    def __init__(self,table):
        self.table = table

    def GetValues(self,sortparameters=[],filterparameters={}):
        pass

    def GetModifityValues(self):
        pass

    def GetValue(self,key):
        pass
