from .abstract_repository import AbstractRepository
class RepositorySessionStatus(AbstractRepository):

    def GetValues(self):
        return ["целевая",
                "пустая"]

    def GetModifityValues(self):
        modifity = []
        for item in self.GetValues():
            modifity.append((item,item))
        return modifity

