import pymysql
import pandas as pd
from sklearn.preprocessing import OneHotEncoder 
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score
from datetime import datetime
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

def getCursor(app):
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
        return cursor,connection
    
def getXY(cursor,request,cols1,cols2,cols3,test_size=0.2,random_state=42,n_clusters=5):
    cursor.execute(request)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=columns)

    if len(cols1)>0:
        encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        x1 = pd.DataFrame(encoder.fit_transform(df[cols1]), columns=encoder.get_feature_names_out(cols1))
        x2=df[cols2]
        x=pd.concat([x1, x2], axis=1)
        categories=dict()
        for col in cols1:
            categories[col] = df[col].unique()
    else:
        x=df[cols2]
        categories=None
        encoder=None
        """if 'startdate' in df.columns:
            df['date'] = pd.to_datetime(df['startdate'], errors='coerce')  # Handle invalid dates with 'coerce'
            today = datetime.today()
            df['days_diff'] = (today - df['date']).dt.days
        """
    if len(cols3)>0:
        y=df[cols3]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)
        return encoder,x_train, x_test, y_train, y_test,categories
    else:
        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(x)
        x_scaled = x_scaled[~np.isnan(x_scaled).any(axis=1)]
        scaled_df = pd.DataFrame(x_scaled, columns=x.columns)

        #x_train, x_test = train_test_split(x, test_size=test_size, random_state=random_state)
        return encoder,scaled_df, None, None,None,categories

    
def train_and_evaluate_model(model, x_train, y_train, x_test, y_test, eval_metric='r2_score',n_clusters=5):
    if not y_train is None:
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        if eval_metric == 'r2_score':
            metric_value = r2_score(y_test, y_pred)
        elif eval_metric == 'mse':
            metric_value = mean_squared_error(y_test, y_pred)
        elif eval_metric == 'accuracy':
            metric_value = accuracy_score(y_test, y_pred)
        else:
            raise ValueError(f"Unsupported evaluation metric: {eval_metric}")
        return model, metric_value, y_pred
    else:
        if isinstance(model, KMeans):
            instan=KMeans(n_clusters=5, random_state=42)
            instan.fit(x_train)
            y_pred = instan.predict(x_train)
            metric_value=0
        if eval_metric == 'Silhouette':
            metric_value = silhouette_score(x_train, y_pred)
        return instan, metric_value, y_pred

def train_predictor(app,model_class,classifier,n_clusters=5):
    cursor,connection=getCursor(app)
    request="""select pt.paymenttypetitle,amount,TIMESTAMPDIFF(SECOND, p.paymentdate, p.createdat) as secondes,ot.title
        from payment p inner join
        payment_type pt on pt.ID=p.paymenttypeid
        inner join organization o
        on o.id=p.organizationid
        inner join organization_type ot
        on ot.id=o.organizationtypeid
        where paymenttypetitle in ('Chèque','Virement bancaire')"""
    test_size=0.2
    random_state=42
    cols1=['paymenttypetitle','title']
    cols2=['amount']
    cols3=['secondes']
    model = classifier()
    eval_metric='r2_score'
    encoder,x_train, x_test, y_train, y_test,categories=getXY(cursor,request,cols1,cols2,cols3,test_size,random_state,5)
    model, metric_value, y_pred=train_and_evaluate_model(model, x_train, y_train, x_test, y_test, eval_metric,5)
    cursor.close()
    connection.close()
    return model_class(model,encoder,metric_value,eval_metric,cols1,cols2,cols3,request,categories,n_clusters)

def train_predictor_c(app,model_class,classifier,n_clusters=5):
    cursor,connection=getCursor(app)
    request="""select o.ID, 
       o.operatingbudget, 
       ot.title, 
       s.startdate, 
       pt.autopayment,
       COALESCE(p2.paysum, 0) as paysum,
       COALESCE(p2.paycount, 0) as paycount,
       COALESCE(a2.c, 0) as articlecount,
       COALESCE(j2.c, 0) as jobcount,
       COALESCE(c2.c, 0) as coursecount,
       COALESCE(e2.c, 0) as eventcount,
       DATEDIFF(CURDATE(), s.startdate) as days_diff
        from organization o
        inner join organization_type ot
            on ot.id = o.organizationtypeid
        inner join subscription s
            on o.subscriptionid = s.id
        inner join payment_type pt
            on pt.id = s.paymenttypeid
        left join (
            select organizationid, 
                sum(amount) as paysum, 
                count(amount) as paycount 
            from payment p
            group by organizationid
        ) p2
            on p2.organizationid = o.id
        left join (
            select organizationid, 
                count(id) as c 
            from article a
            group by organizationid
        ) a2
            on a2.organizationid = o.id
        left join (
            select organizationid, 
                count(id) as c 
            from job j
            group by organizationid
        ) j2
            on j2.organizationid = o.id
        left join (
            select organizationid, 
                count(id) as c 
            from course c
            group by organizationid
        ) c2
            on c2.organizationid = o.id
        left join (
            select organizationid, 
                count(id) as c 
            from planned_event e
            group by organizationid
        ) e2
            on e2.organizationid = o.id
        where ot.title = 'MRC'
            """
    test_size=0.2
    random_state=42
    n_clusters=5
    cols1=['autopayment']
    cols2=['operatingbudget'#,'servedpopulation'
               ,'days_diff','paycount','paysum','articlecount','jobcount','coursecount','eventcount']
    model = classifier()
    eval_metric='silhouette'
    encoder,x_train, x_test, y_train, y_test,categories=getXY(cursor,request,cols1,cols2,[],test_size,random_state,n_clusters)
    model, metric_value, y_pred=train_and_evaluate_model(model, x_train, y_train, x_test, y_test, eval_metric, n_clusters)
    cursor.close()
    connection.close()
    return model_class(model,encoder,metric_value,eval_metric,cols1,cols2,[],request,categories,n_clusters)


def train_predictor_cust(app,model_class,classifier,req,test_size,random_state,cols1,cols2,cols3,eval_metric,n_clusters=5):
    cursor,connection=getCursor(app)
    model = classifier()
    encoder,x_train, x_test, y_train, y_test,categories=getXY(cursor,req,cols1,cols2,cols3,test_size,random_state,n_clusters)
    model, metric_value, y_pred=train_and_evaluate_model(model, x_train, y_train, x_test, y_test, eval_metric,5)
    cursor.close()
    connection.close()
    return model_class(model,encoder,metric_value,eval_metric,cols1,cols2,cols3,req,categories,n_clusters)