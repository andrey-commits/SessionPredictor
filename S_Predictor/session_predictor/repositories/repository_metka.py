from .abstract_repository import AbstractRepository
from ..models import Session

class RepositoryMetka(AbstractRepository):
    def GetValues(self):
        return sorted(set([s.label for s in list(Session.objects.filter(delete_status = False).exclude(label__isnull=True).exclude(label__exact=''))]))
