from django.conf import settings
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from .helpers.filter_helper import FilterCleaner
from .helpers.field_helper import FieldHelper
from .resolvers.resolver_filter import FilterResolver
from .resolvers.resolver_sorter import SortResolver
from .resolvers.resolver_repository import RepositoryResolver
from .executors.executor_label import LabelExecutor
from .executors.executor_delete import DeleteExecutor
from .executors.executor_session_data import DataExecutor


def index(request):
    return redirect('hauptview', errordata = 0)

def hauptview(request, errordata):
    data = { "errordata" : errordata }
    filterparameters = {}
    sortparameters = []
    filterResolver = FilterResolver()
    sorterResolver = SortResolver()
    repositoryResolver = RepositoryResolver()
    for field in FieldHelper.GetFields():
        repository = repositoryResolver.GetHandler(field)
        filter = filterResolver.GetHandler(field)
        sorter = sorterResolver.GetHandler(field)
        if(repository is not None):
            data[f"{field}_values"] = repository.GetValues()
        if(filter is not None):
            data[f"{field}_filter_value"] = filter.FilterInit()
            if((data[f"{field}_filter_value"] is not None) & ((data[f"{field}_filter_value"]!=""))):
                filterparameters[f"{field}"] = data[f"{field}_filter_value"]
        if(sorter is not None):
            data[f"sort_{field}"] = sorter.SorterInit()
            if ((data[f"sort_{field}"] is not None) & ((data[f"sort_{field}"] != ""))):
                if(data[f"sort_{field}"]=="⭣"):
                    sortparameters.append(field)
                if (data[f"sort_{field}"] == "⭡"):
                    sortparameters.append(f"-{field}")
    repository = repositoryResolver.GetHandler('sessions')
    sessions = repository.GetValues(sortparameters = sortparameters,filterparameters = filterparameters)
    set_label = request.POST.get("set_label")
    if((set_label is not None) & (set_label!="")):
        label_executor = LabelExecutor('Session')
        for session in sessions:
            label_executor.Execute(session.id,set_label)
        return redirect('hauptview', errordata = 0)
    deleter_apply = request.POST.get("delete")
    if(deleter_apply == "del"):
        delete_executor = DeleteExecutor('Session')
        for session in sessions:
            delete_executor.Execute(session.id)
        return redirect('hauptview', errordata=0)
    data['sessions'] = sessions
    return TemplateResponse(request,"HauptView.html",data)

def roc_aucview(request):
    return render(request,"Roc_AucView.html")

def journalview(request):
    return render(request,"JournalView.html")

def filterexecutor(request):
    filterResolver = FilterResolver()
    for field in FieldHelper.GetFields():
        value = request.POST.get(field)
        filter = filterResolver.GetHandler(field)
        if(filter is not None):
            filter.FilterApply(value)
    return redirect('hauptview', errordata = 0)

def filtercleaner(request):
    FilterCleaner()
    return redirect('hauptview', errordata = 0)

def sorterexecutor(request):
    sorterResolver = SortResolver()
    for field in FieldHelper.GetFields():
        if (request.POST.get(f"sort_{field}") == 'sort'):
            sorter = sorterResolver.GetHandler(field)
            sorter.SorterApply()
    return redirect('hauptview', errordata = 0)

def loaddata(request):
    try:
        path = f"{settings.LOAD_DATA}/{request.FILES['filedata'].name}"
        if(path[-3:]!="csv"):
            return redirect('hauptview',errordata = 1)
        with open(path, "wb+") as destination:
            destination.write(request.FILES['filedata'].read())
        label = request.POST.get('labeldata')
        executor = DataExecutor('Session')
        executor.Execute(path,label)
    except:
        return redirect('hauptview', errordata = 1)
    return redirect('hauptview',errordata = 0)

