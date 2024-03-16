from .abstract_resolver import AbstractResolver
from ..sorters.sorter_custom import SorterCustom
from ..sorters.abstract_sorter import AbstractSorter

class SortResolver(AbstractResolver):
    def GetHandler(self,field):
        if (field in ['metka',
                'session_status',
                'predict_session_status',
                'utm_source',
                'utm_medium',
                'utm_campaign',
                'utm_adcontent',
                'utm_keyword',
                'device_brand',
                'device_screen_resolution',
                'geo_city',
                'visit_number',
                'date']):
            return SorterCustom(field)
        return None

