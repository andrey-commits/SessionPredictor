from django.urls import path
from .import views

urlpatterns = [
    path('hauptview/0/loaddata/',views.loaddata, name = 'loaddata'),
    path('hauptview/1/loaddata/',views.loaddata, name = 'loaddata'),
    path('filtercleaner/',views.filtercleaner, name = 'filtercleaner'),
    path('hauptview/0/filterexecutor/',views.filterexecutor, name = 'filterexecutor'),
    path('hauptview/1/filterexecutor/',views.filterexecutor, name = 'filterexecutor'),
    path('hauptview/0/sorterexecutor/',views.sorterexecutor, name = 'sorterexecutor'),
    path('hauptview/1/sorterexecutor/',views.sorterexecutor, name = 'sorterexecutor'),
    path('rocauc/',views.roc_aucview, name = 'roc_aucview'),
    path('journal/',views.journalview, name = 'journalview'),
    path('hauptview/<int:errordata>/',views.hauptview, name = 'hauptview'),
    path('', views.index, name='home')
]