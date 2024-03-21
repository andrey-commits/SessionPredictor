from sklearn.ensemble import RandomForestClassifier
import sqlite3
import pandas as pd
import joblib
from sklearn.metrics import roc_auc_score



FEATURES = ['utm_source',
                'utm_medium',
                'utm_campaign',
                'utm_adcontent',
                'utm_keyword',
                'device_brand',
                'device_screen_resolution',
                'geo_city']

def Categorial_Encoder(data):
    def GetEncodingDictionary(table):
        connect = sqlite3.connect(f"./static/categorial_features.db")
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
        encoder = joblib.load(f"./static/{feature}_encoder.pkl")
        data_new = pd.DataFrame(encoder.transform(data[[feature]]).toarray(), columns=encoder.categories_)
        columns_new = []
        for k in range(0, len(data_new.columns)):
            columns_new.append(f"{data_new.columns[k][0]}_{feature}")
        data_new.columns = columns_new
        data = data.drop(columns=[feature])
        data = data.join(data_new)
    return data

data = pd.read_csv('./uploads/session_data_sauber.csv')

data = data[(data.isna().any(axis = 1)==False)]

data = data[['visit_number','utm_source',
             'utm_medium',
             'utm_campaign',
             'utm_adcontent',
             'utm_keyword',
             'device_brand',
             'device_screen_resolution',
             'geo_city','session_status']]

data = Categorial_Encoder(data)

data = Feature_Encoder(data)

x = data.drop(columns=['session_status'])
Y = data['session_status']


forest_clf = RandomForestClassifier(random_state=42,n_estimators=40,max_depth=40,max_features=12,class_weight='balanced')

forest_clf.fit(x,Y)

y_probas = forest_clf.predict(x)

score = roc_auc_score(Y,y_probas)

joblib.dump(forest_clf, './static/Session_predictor.pkl')

print(score)




