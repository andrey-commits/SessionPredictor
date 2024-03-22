from .abstract_resolver import AbstractResolver
from ..filters.filter_feature import FilterFeature
from ..filters.filter_other import FilterOther
from ..filters.filter_alternative import FilterAlternativeNumber
from ..filters.filter_alternative import FilterAlternativeDate

class FilterResolver(AbstractResolver):
    def GetHandler(self,field):
        if field in ['utm_source',
                'utm_medium',
                'utm_campaign',
                'utm_adcontent',
                'utm_keyword',
                'device_brand',
                'device_screen_resolution',
                'geo_city']:
            return FilterFeature(field)
        if field in ['metka',
                'session_status',
                'predict_session_status']:
            return FilterOther(field)
        if field in ['begin_date',
                      'end_date']:
            return FilterAlternativeDate(field)
        if field in ['visit_number']:
            return FilterAlternativeNumber(field)
        return None