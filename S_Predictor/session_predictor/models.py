from django.db import models
from .repositories.repository_feature import RepositoryFeature
from .repositories.repository_session_status import RepositorySessionStatus
import datetime
class Session(models.Model):
    class Meta:
        db_table = "sessions"
    id = models.AutoField(primary_key = True)
    label = models.TextField(blank=True,null=True)
    date = models.DateField(auto_now_add=True)
    visit_number = models.IntegerField(default = 1)
    utm_source = models.CharField(max_length=200,choices = RepositoryFeature('utm_source').GetModifityValues(),blank=False)
    utm_medium = models.CharField(max_length=200, choices = RepositoryFeature('utm_medium').GetModifityValues(),blank=False)
    utm_campaign = models.CharField(max_length=200, choices = RepositoryFeature('utm_campaign').GetModifityValues(),blank=False)
    utm_adcontent = models.CharField(max_length=200,choices = RepositoryFeature('utm_adcontent').GetModifityValues(),blank=False)
    utm_keyword = models.CharField(max_length=200,choices = RepositoryFeature('utm_keyword').GetModifityValues(),blank=False)
    device_brand = models.CharField(max_length=200,choices = RepositoryFeature('device_brand').GetModifityValues(),blank=False)
    device_screen_resolution = models.CharField(max_length=200,choices = RepositoryFeature('device_screen_resolution').GetModifityValues,blank=False)
    geo_city = models.CharField(max_length=200,choices = RepositoryFeature('geo_city').GetModifityValues,blank=False)
    session_status = models.CharField(max_length=50,choices=RepositorySessionStatus('session_status').GetModifityValues(),blank=False)
    predict_session_status = models.CharField(max_length=50,choices=RepositorySessionStatus('predict_session_status').GetModifityValues(),null=True)
    delete_status = models.BooleanField(default=False)

    @property
    def getDate(self):
        return self.date.strftime('%d.%m.%Y')

    @property
    def getPStatusView(self):
        if(self.predict_session_status==None):
            return ""
        return self.predict_session_status

class JournalNote(models.Model):
    class Meta:
        db_table = "journalnotes"
    id = models.AutoField(primary_key = True)
    session_id = models.IntegerField(blank = False)
    date = models.DateField(auto_now_add=True)
    operation = models.TextField(default="сессия не установлена")

