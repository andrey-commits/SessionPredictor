from .abstract_repository import AbstractRepository
from ..models import JournalNote

class RepositoryJournalMetka(AbstractRepository):
    def GetValues(self):
        return sorted(set([j.session_label for j in list(JournalNote.objects.exclude(session_label__isnull=True).exclude(session_label__exact=''))]))
