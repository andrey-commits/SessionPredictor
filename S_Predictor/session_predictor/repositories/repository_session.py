import datetime

from .abstract_repository import AbstractRepository
from ..models import Session

class RepositorySession(AbstractRepository):

    def GetValues(self,sortparameters=[],filterparameters={}):
        filterparameters['delete_status'] = False
        if ("metka" in filterparameters.keys()):
            filterparameters["label"] = filterparameters["metka"]
            del filterparameters["metka"]
        if(("begin_date" in filterparameters.keys())==False):
            filterparameters["begin_date"] = datetime.datetime.now()
        if (("end_date" in filterparameters.keys()) == False):
            filterparameters["end_date"] = datetime.datetime.now()
        sessions = Session.objects.filter(date__gt=filterparameters["begin_date"]) & Session.objects.filter(date__lt=filterparameters["end_date"])
        del filterparameters["begin_date"]
        del filterparameters["end_date"]
        if ("metka" in sortparameters):
            sortparameters.append("label")
            sortparameters.remove("metka")
        if ("-metka" in sortparameters):
            sortparameters.append("-label")
            sortparameters.remove("-metka")
        sessions = sessions.filter(**filterparameters).order_by(*sortparameters)
        return sessions
    def GetValue(self,key):
        session = Session.objects.get(id=key)
        return session
