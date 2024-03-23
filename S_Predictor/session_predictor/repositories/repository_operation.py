from .abstract_repository import AbstractRepository
from ..models import JournalNote

class RepositoryOperation(AbstractRepository):
    def GetValues(self):
        return sorted(set([j.operation for j in JournalNote.objects.all()]))