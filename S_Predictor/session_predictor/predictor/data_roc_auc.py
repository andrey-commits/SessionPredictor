import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import datetime
from sklearn.metrics import roc_auc_score, roc_curve
from ..models import Session
import xml.etree.ElementTree as ET
from django.conf import settings




def MetricApply():
    status_morphy = { 'целевая': 1,
                      'пустая': 0 }
    sessions = Session.objects.filter(delete_status = False).exclude(predict_session_status__exact=None,session_status__exact=None)
    predicts = [status_morphy[s.session_status] for s in list(sessions)]
    predicts_proba = [status_morphy[s.predict_session_status] for s in list(sessions)]
    value_metric = roc_auc_score(predicts,predicts_proba)
    fpr,tpr,tresholds = roc_curve(predicts,predicts_proba)

    plt.plot(fpr, tpr,linewidth=2,c='blue')
    plt.plot([0,1],[0,1],'k--')
    plt.savefig(f"{settings.STATIC_ROOT}/metric.jpg")

    tree = ET.parse(f"{settings.PREDICTOR_DATA}/MetricData.xml")
    root = tree.getroot()
    node_v = root.find("value")
    node_v.text = f'{value_metric:.2f}'
    node_d = root.find("date")
    node_d.text = datetime.datetime.now().strftime('%d.%m.%Y')
    tree.write(f"{settings.PREDICTOR_DATA}/MetricData.xml")

def GetMetricData():
    tree = ET.parse(f"{settings.PREDICTOR_DATA}/MetricData.xml")
    root = tree.getroot()
    metric_data = {'metric_value':"",
                   'metric_date':""}
    if(root.find("value").text is not None):
        metric_data['metric_value'] = root.find("value").text
    if(root.find("date").text is not None):
        metric_data['metric_date'] = root.find("date").text
    return metric_data