from .abstract_executor import AbstractExecutor
from ..models import JournalNote

class JournalExecutor(AbstractExecutor):
    def Execute(self,object,label):
        JournalNote.objects.create(session_id = object.id,
                                   session_label = object.label,
                                   session_date = object.date,
                                   operation = label)