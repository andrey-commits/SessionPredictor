from .repositories.repository_feature import RepositoryFeature
from .repositories.repository_session_status import RepositorySessionStatus
from django import forms
from .models import Session

class SessionForm(forms.ModelForm):
    label = forms.CharField(max_length=200,label = "метка")
    visit_number = forms.IntegerField(required=True, label = "visit_number")
    utm_source = forms.ChoiceField(choices = RepositoryFeature('utm_source').GetModifityValues(), widget=forms.widgets.Select, label="utm_source")
    utm_medium = forms.ChoiceField(choices = RepositoryFeature('utm_medium').GetModifityValues(), widget=forms.widgets.Select, label ="utm_medium")
    utm_campaign = forms.ChoiceField(choices = RepositoryFeature('utm_campaign').GetModifityValues(),widget=forms.widgets.Select, label ="utm_campaign")
    utm_adcontent = forms.ChoiceField(choices = RepositoryFeature('utm_adcontent').GetModifityValues(),widget=forms.widgets.Select, label ="utm_adcontent")
    utm_keyword = forms.ChoiceField(choices = RepositoryFeature('utm_keyword').GetModifityValues(),widget=forms.widgets.Select, label ="utm_keyword")
    device_brand = forms.ChoiceField(choices = RepositoryFeature('device_brand').GetModifityValues(),widget=forms.widgets.Select, label ="device_brand")
    device_screen_resolution = forms.ChoiceField(choices = RepositoryFeature('device_screen_resolution').GetModifityValues(),widget=forms.widgets.Select, label ="device_screen_resolution")
    geo_city = forms.ChoiceField(choices = RepositoryFeature('geo_city').GetModifityValues,widget=forms.widgets.Select, label ="geo_city")
    session_status = forms.ChoiceField(choices = RepositorySessionStatus('session_status').GetModifityValues(),widget=forms.widgets.Select, label ="session_status")

    class Meta:
        model = Session
        fields = ('label',
                  'visit_number',
                  'utm_source',
                  'utm_medium',
                  'utm_campaign',
                  'utm_adcontent',
                  'utm_keyword',
                  'device_brand',
                  'device_screen_resolution',
                  'geo_city',
                  'session_status')