from .abstract_repository import AbstractRepository
from ..models import Session

class RepositoryMetka(AbstractRepository):
    def GetValues(self):
        return set([s.label for s in Session.objects.filter(delete_status = False).distinct()])
