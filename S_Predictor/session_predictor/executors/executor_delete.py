from .abstract_executor import AbstractExecutor
from .executor_journal import JournalExecutor
from ..models import Session

class DeleteExecutor(AbstractExecutor):

    def Execute(self,object):
        Session.objects.filter(id = object).update(delete_status = True)
        journal_executor = JournalExecutor('JournalNote')
        journal_executor.Execute(object,"запись удалена")