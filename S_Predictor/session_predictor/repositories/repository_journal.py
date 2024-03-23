import datetime
from .abstract_repository import AbstractRepository
from ..models import JournalNote

class RepositoryJournals(AbstractRepository):

    def GetValues(self,filterparameters={}):
        if ("metka" in filterparameters.keys()):
            filterparameters["session_label"] = filterparameters["metka"]
            del filterparameters["metka"]
        if(("begin_date" in filterparameters.keys())==False):
            filterparameters["begin_date"] = datetime.datetime.now()
        if (("end_date" in filterparameters.keys()) == False):
            filterparameters["end_date"] = datetime.datetime.now()
        journals = JournalNote.objects.filter(date__gt=filterparameters["begin_date"]) & JournalNote.objects.filter(date__lt=filterparameters["end_date"])
        del filterparameters["begin_date"]
        del filterparameters["end_date"]
        journals = journals.filter(**filterparameters).order_by("-date")
        return journals