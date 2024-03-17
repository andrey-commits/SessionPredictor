from .abstract_executor import AbstractExecutor
import pandas as pd
from ..models import Session
from ..resolvers.resolver_repository import RepositoryResolver
from .executor_journal import JournalExecutor

class DataExecutor(AbstractExecutor):
    def Execute(self,object,label):
        data = pd.read_csv(object)
        for index,row in data.iterrows():
            resolver = RepositoryResolver()
            status_repository = resolver.GetHandler('session_status')
            session_status = status_repository.GetValues()[1-row['session_status']]
            session = Session.objects.create(label = label,
                                            visit_number = row['visit_number'],
                                            utm_source = row['utm_source'],
                                            utm_campaign = row['utm_campaign'],
                                            utm_adcontent = row['utm_adcontent'],
                                            utm_medium = row['utm_medium'],
                                            utm_keyword = row['utm_keyword'],
                                            device_brand = row['device_brand'],
                                            device_screen_resolution = row['device_screen_resolution'],
                                            geo_city = row['geo_city'],
                                            session_status = session_status)
            journal_executor = JournalExecutor('Data')
            journal_executor.Execute(object = session,label = "сессия добавлена")