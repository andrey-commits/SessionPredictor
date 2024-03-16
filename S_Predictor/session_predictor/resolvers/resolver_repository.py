from .abstract_resolver import AbstractResolver
from ..repositories.repository_feature import RepositoryFeature
from ..repositories.repository_session_status import RepositorySessionStatus
from ..repositories.repository_session import RepositorySession
from ..repositories.repository_metka import RepositoryMetka
from ..repositories.abstract_repository import AbstractRepository
['metka',

'visit_number',
                'begin_date',
                'end_date',
                'date']
class RepositoryResolver(AbstractResolver):

    def GetHandler(self,field):
        if field in ['metka']:
            return RepositoryMetka('metka')
        if field in ['utm_source',
                'utm_medium',
                'utm_campaign',
                'utm_adcontent',
                'utm_keyword',
                'device_brand',
                'device_screen_resolution',
                'geo_city']:
            return RepositoryFeature(field)
        if field in ['session_status',
                'predict_session_status']:
            return RepositorySessionStatus(field)
        if field in ['sessions']:
            return RepositorySession(field)
        return None
