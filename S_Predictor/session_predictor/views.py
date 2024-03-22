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
from .executors.executor_session import SessionExecutor
from .forms import SessionForm
from .predictor.data_predictor import Predict
from .predictor.data_roc_auc import MetricApply, GetMetricData


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
    sessions = repository.GetValues(sortparameters=sortparameters, filterparameters=filterparameters)
    set_label = request.POST.get("set_label")
    if((set_label is not None) & (set_label!="")):
        label_executor = LabelExecutor('Session')
        for session in sessions:
            label_executor.Execute(object = session,label = set_label)
        return redirect('hauptview', errordata = 0)
    deleter_apply = request.POST.get("delete")
    if(deleter_apply == "del"):
        delete_executor = DeleteExecutor('Session')
        for session in sessions:
            delete_executor.Execute(object = session)
        return redirect('hauptview', errordata=0)
    predictor_apply = request.POST.get("prediction")
    if(predictor_apply =="predict"):
        try:
            if(sessions.filter(predict_session_status__exact=None).exists()):
                unpredict_sessions = sessions.filter(predict_session_status__exact=None)
                list_sessions = list(unpredict_sessions)
                Predict(list_sessions)
        except:
            return redirect('hauptview', errordata=1)
        return redirect('hauptview', errordata=0)
    n_sessions = len(sessions)
    page_number = 0
    menge_sessions = 0
    if (n_sessions<=500):
        page_number = 0
        menge_sessions = n_sessions
    elif(n_sessions>500):
        if((request.POST.get("page_number") is not None) and (int(request.POST.get("page_number")) > 0)):
            page_number = int(request.POST.get("page_number"))-1
        if (page_number > n_sessions):
            menge_sessions = 0
        if((page_number+500) > n_sessions):
            menge_sessions = n_sessions - page_number
        if((page_number+500) <= n_sessions):
            menge_sessions = 500
    data['page_number'] = page_number+1
    data['menge_sessions'] = menge_sessions
    data['n_sessions'] = n_sessions
    data['sessions'] = sessions[page_number:(page_number+500)]
    return TemplateResponse(request,"HauptView.html",data)

def roc_aucview(request):
    data = GetMetricData()
    if(request.POST.get("metric_apply") == "apply"):
        MetricApply()
    return TemplateResponse(request,"Roc_AucView.html",data)

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
        if(label is None):
            label = ""
        executor = DataExecutor('Session')
        executor.Execute(path,label)
    except:
        return redirect('hauptview', errordata = 1)
    return redirect('hauptview',errordata = 0)

def sessionexecutor(request):
    operation =""
    select_session_id =-1
    form = SessionForm(initial={'visit_number': 1})
    if(request.POST.get("operation_session")=="add"):
        operation = "Добавить сессию"
    if (request.POST.get("operation_session") == "redact"):
        operation = "Изменить сессию"
        repositoryResolver = RepositoryResolver()
        repository = repositoryResolver.GetHandler('sessions')
        select_session_id = request.POST.get('select-session-id')
        session = repository.GetValue(request.POST.get('select-session-id'))
        form = SessionForm(initial={'label': session.label,
                                    'visit_number': session.visit_number,
                                    'utm_source': session.utm_source,
                                    'utm_medium': session.utm_medium,
                                    'utm_campaign': session.utm_campaign,
                                    'utm_keyword': session.utm_keyword,
                                    'device_brand': session.device_brand,
                                    'device_screen_resolution': session.device_screen_resolution,
                                    'geo_city': session.geo_city,
                                    'session_status': session.session_status})
    data = {"form" : form,
            "operation" : operation,
            "select_session_id" : select_session_id}
    return TemplateResponse(request,"SessionView.html",data)

def session_executor_apply(request):
    data = {}
    select_session_id = request.POST.get('select_session_id')
    data["label"] = request.POST.get("label")
    data["visit_number"] = request.POST.get("visit_number")
    data["utm_source"] = request.POST.get("utm_source")
    data["utm_medium"] = request.POST.get("utm_medium")
    data["utm_campaign"] = request.POST.get("utm_campaign")
    data["utm_adcontent"] = request.POST.get("utm_adcontent")
    data["utm_keyword"] = request.POST.get("utm_keyword")
    data["device_brand"] = request.POST.get("device_brand")
    data["device_screen_resolution"] = request.POST.get("device_screen_resolution")
    data["geo_city"] = request.POST.get("geo_city")
    data["session_status"] = request.POST.get("session_status")
    executor = SessionExecutor('Session')
    executor.Execute(data, select_session_id)
    return redirect('hauptview',errordata = 0)




