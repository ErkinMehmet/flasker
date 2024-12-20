import pymysql
import pandas as pd
from sklearn.preprocessing import OneHotEncoder 
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score


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
    
def getXY(cursor,request,cols1,cols2,cols3,test_size=0.2,random_state=42):
    cursor.execute(request)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=columns)
    if len(cols1)>0 and len(cols3)>0:
        encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        x1 = pd.DataFrame(encoder.fit_transform(df[cols1]), columns=encoder.get_feature_names_out(cols1))
        x2=df[cols2]
        x=pd.concat([x1, x2], axis=1)
        y=df[cols3]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)
        return encoder,x_train, x_test, y_train, y_test
    elif len(cols3)>0:
        x=df[cols2]
        y=df[cols3]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)
        return None,x_train, x_test, y_train, y_test
    else:
        pass # non supervisé
    
def train_and_evaluate_model(model, x_train, y_train, x_test, y_test, eval_metric='r2_score'):
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

def train_predictor(app,model_class,classifier):
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
    encoder,x_train, x_test, y_train, y_test=getXY(cursor,request,cols1,cols2,cols3,test_size,random_state)
    model, metric_value, y_pred=train_and_evaluate_model(model, x_train, y_train, x_test, y_test, eval_metric='r2_score')
    cursor.close()
    connection.close()
    return model_class(model,encoder,metric_value,eval_metric,cols1,cols2,cols3,request)