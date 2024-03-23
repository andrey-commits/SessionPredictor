from .abstract_resolver import AbstractResolver
from ..filters.filter_other import FilterOther
from ..filters.filter_alternative import FilterAlternativeDate

class FilterJournalResolver(AbstractResolver):
    def GetHandler(self,field):
        if field in ['begin_date',
                     'end_date']:
            return FilterAlternativeDate(field)
        if field in ['metka',
                     'operation']:
            return FilterOther(field)
        return None