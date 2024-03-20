from django.conf import settings
import os
import sqlite3
import pandas as pd
from ..models import Session
import joblib
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline
from ..resolvers.resolver_repository import RepositoryResolver
from ..executors.executor_journal import JournalExecutor


FEATURES = ['utm_source',
                'utm_medium',
                'utm_campaign',
                'utm_adcontent',
                'utm_keyword',
                'device_brand',
                'device_screen_resolution',
                'geo_city']

def GetData(sessions):
    return pd.DataFrame.from_records([session.to_dict() for session in sessions])
def Categorial_Encoder(data):
    def GetEncodingDictionary(table):
        connect = sqlite3.connect(os.path.join(settings.STATIC_ROOT, 'categorial_features.db'))
        data = pd.read_sql_query(
            f"SELECT * FROM {table} WHERE Name NOT IN ('negative_value','positive_value') ORDER BY Name",
            connect)
        connect.close()
        result = {}
        for index, row in data.iterrows():
            result[row['Name']] = int(row['Id'])
            if ((row['secondary_value'] is not None) & (row['secondary_value'] != "")):
                result[row['Name']] = int(row['secondary_value'])
        return result
    for feature in FEATURES:
        data[feature] = data[feature].map(GetEncodingDictionary(feature))
    return data

def Feature_Encoder(data):
    for feature in FEATURES:
        encoder = joblib.load(os.path.join(settings.STATIC_ROOT, f"{feature}_encoder.pkl"))
        data_new = pd.DataFrame(encoder.transform(data[[feature]]).toarray(), columns=encoder.categories_)
        columns_new = []
        for k in range(0, len(data_new.columns)):
            columns_new.append(f"{data_new.columns[k][0]}_{feature}")
        data_new.columns = columns_new
        data = data.drop(columns=[feature])
        data = data.join(data_new)
    return data

def WritePrediction(sessions,result):
    index = 0
    for session in sessions:
        resolver = RepositoryResolver()
        status_repository = resolver.GetHandler('session_status')
        session_status = status_repository.GetValues()[1 - result[index]]
        Session.objects.filter(id = session.id).update(predict_session_status = session_status)
        journal_executor = JournalExecutor('session')
        journal_executor.Execute(object=session, label="сессия предиктирована")

get_data = FunctionTransformer(GetData)
categorial_encoder = FunctionTransformer(Categorial_Encoder)
feature_encoder = FunctionTransformer(Feature_Encoder)
model = joblib.load(os.path.join(settings.STATIC_ROOT, 'Session_predictor.pkl'))

steps = [('get_data',get_data),
         ('categorial_encoding',categorial_encoder),
         ('feature_encoding',feature_encoder),
         ('predict',model)]

pipe = Pipeline(steps)
def Predict(sessions):
    result = pipe.predict(sessions)
    return WritePrediction(sessions, result)