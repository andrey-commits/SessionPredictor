from .abstract_executor import AbstractExecutor
from .executor_journal import JournalExecutor
from ..models import Session

class SessionExecutor(AbstractExecutor):
    def Execute(self,object,label):
        journal_executor = JournalExecutor('JournalNote')
        if(int(label) == -1):
            session = Session.objects.create(**object)
            return journal_executor.Execute(object = session,label = "сессия создана")
        Session.objects.filter(id = label).update(**object)
        session = Session.objects.get(id = label)
        return journal_executor.Execute(object = session, label = "сессия изменена")