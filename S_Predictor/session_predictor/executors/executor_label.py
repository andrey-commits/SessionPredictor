from .abstract_executor import AbstractExecutor
from .executor_journal import JournalExecutor
from ..models import Session

class LabelExecutor(AbstractExecutor):

    def Execute(self,object,label):
        Session.objects.filter(id = object).update(label = label)
        journal_executor = JournalExecutor('JournalNote')
        journal_executor.Execute(object,f"установлена метка:{label}")

