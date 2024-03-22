from django.conf import settings
import os
import sqlite3
import pandas as pd
from .abstract_repository import AbstractRepository

class RepositoryFeature(AbstractRepository):
    def GetValues(self):
        connect = sqlite3.connect(os.path.join(settings.STATIC_ROOT,'categorial_features.db'))
        data = pd.read_sql_query(f"SELECT Id,Name FROM {self.table} WHERE Name NOT IN ('negative_value','positive_value','nan') ORDER BY Name",connect)
        connect.close()
        result = {}
        for index,row in data.iterrows():
            result[row['Id']] = row['Name']
        return result

    def GetModifityValues(self):
        modifity = []
        for value in self.GetValues().values():
            modifity.append((value,value))
        return modifity