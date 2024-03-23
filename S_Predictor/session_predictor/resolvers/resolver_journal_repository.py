from .abstract_resolver import AbstractResolver
from ..repositories.repository_journal_metka import RepositoryJournalMetka
from ..repositories.repository_journal import RepositoryJournals
from ..repositories.repository_operation import RepositoryOperation

class RepositoryJournalResolver(AbstractResolver):
    def GetHandler(self,field):
        if field in ['metka']:
            return RepositoryJournalMetka(field)
        if field in ['operation']:
            return RepositoryOperation(field)
        if field in ['journals']:
            return RepositoryJournals(field)
        return None