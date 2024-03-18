from django.conf import settings
import os
import sqlite3
import pandas as pd
class Preprocessor:
    def GetEncodingDictionary(self,table):
        connect = sqlite3.connect(os.path.join(settings.STATIC_ROOT, 'categorial_features.db'))
        data = pd.read_sql_query(
            f"SELECT * FROM {table} WHERE Name NOT IN ('negative_value','positive_value') ORDER BY Name",
            connect)
        connect.close()
        result = {}
        for index, row in data.iterrows():
            result[row['Name']] = row['Id']
            if((row['secondary_value'] is not None) & (row['secondary_value']!="")):
                result[row['Name']] = row['secondary_value']
        return result

    def GetOneHotEncoder(self):
        pass

    def ApplyPreprocessing(self,data):
        pass