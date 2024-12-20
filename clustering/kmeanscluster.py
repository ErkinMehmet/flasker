from sklearn.cluster import KMeans
import pymysql
import pandas as pd
from sklearn.preprocessing import OneHotEncoder 
from datetime import datetime
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from flasker.regressors.predictor import Prediction
import numpy as np

class KMeansClustering:
    def __init__(self, model: KMeans, encoder: OneHotEncoder,scaler:StandardScaler,scaled_df) -> None:
        self.model = model
        self.x_scaled=scaled_df
        self.encoder=encoder
        self.scaler=scaler
        self.n=None
        self.random_state=None
        self.labels=None
        #print(scaled_df.head(5))

    def predict(self, input):
        pass
    
    def train(self,n=5,random_state=42):
        self.model.n_clusters = n
        self.model.random_state = random_state
        self.model.fit(self.x_scaled)
        self.labels= self.model.labels_
        sil_score = silhouette_score(self.x_scaled, self.labels)
        return (self.labels,sil_score)


def initiate_kmc_predictor(app) :
    #-> Predictor:
    with app.app_context():
        connection_string = app.config['BDQM']
    if connection_string:
        components = connection_string.split(';')
        db_params = {}
        for component in components:
            if component:
                key, value = component.split('=', 1)
                db_params[key.strip()] = value.strip()
        host = db_params.get('SERVER')
        user = db_params.get('UID')
        password = db_params.get('PWD')
        database = db_params.get('DATABASE')
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        cursor = connection.cursor()

        cursor.execute("""select o.ID,o.operatingbudget,o.servedpopulation,ot.title,s.startdate,pt.autopayment
            ,COALESCE(p2.paysum, 0) as paysum
            ,COALESCE(p2.paycount, 0) as paycount
            ,COALESCE( a2.c, 0)  as articlecount
            , COALESCE(j2.c, 0)  as jobcount
            ,COALESCE(c2.c, 0)  as coursecount,COALESCE(e2.c, 0)  as eventcount
            from organization o
            inner join organization_type ot
            on ot.id=o.organizationtypeid
            inner join subscription s
            on o.subscriptionid=s.id
            inner join payment_type pt
            on pt.id=s.paymenttypeid
            left join (
            select organizationid,sum(amount) as paysum,count(amount) as paycount from payment p
            group by organizationid
            ) p2
            on p2.organizationid=o.id
            left join (
            select organizationid,count(id) as c from article a
            group by organizationid
            ) a2
            on a2.organizationid=o.id
            left join (
            select organizationid,count(id) as c from job j
            group by organizationid
            ) j2
            on j2.organizationid=o.id
            left join (
            select organizationid,count(id) as c from course c
            group by organizationid
            ) c2
            on c2.organizationid=o.id
            left join (
            select organizationid,count(id) as c from planned_event e
            group by organizationid
            ) e2
            on e2.organizationid=o.id
            where ot.title='MRC'
            """)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        df['date'] = pd.to_datetime(df['startdate'])
        today = datetime.today()
        df['days_diff'] = (today - df['startdate']).dt.days
        encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        cols1=['autopayment']
        cols2=['operatingbudget'#,'servedpopulation'
               ,'days_diff','paycount','paysum','articlecount','jobcount','coursecount','eventcount']
        x1 = pd.DataFrame(encoder.fit_transform(df[cols1]), columns=encoder.get_feature_names_out(cols1))
        x2=df[cols2]
        x=pd.concat([x1, x2], axis=1)
        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(x)
        x_scaled = x_scaled[~np.isnan(x_scaled).any(axis=1)]
        scaled_df = pd.DataFrame(x_scaled, columns=x.columns)
        kmeans = KMeans()
        cursor.close()
        connection.close()
        return KMeansClustering(kmeans,encoder,scaler,scaled_df)
