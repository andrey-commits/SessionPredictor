from .abstract_executor import AbstractExecutor
from ..models import JournalNote

class JournalExecutor(AbstractExecutor):
    def Execute(self,object,label):
        journal_note = JournalNote.objects.create(session_id = object,
                                                    operation = label)