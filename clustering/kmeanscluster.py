from sklearn.cluster import KMeans
import pymysql
import pandas as pd
from sklearn.preprocessing import OneHotEncoder 
from datetime import datetime
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from flasker.regressors.predictor import Prediction,Predictor
import numpy as np
from typing import List, Tuple, Optional, cast

class KMeansClustering(Predictor):
    """
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
    """
    def __init__(self, model: KMeans, encoder, metric, 
                 metric_name, cols1, cols2, cols3, req,categories,n_clusters=5) -> None:
        super().__init__(model, encoder, metric, metric_name, cols1, cols2, [], req,categories,n_clusters=5) #obj.extra_properties["n_clusters"]

    def train(self,n=5,random_state=42):
        self.model.n_clusters = n
        self.model.random_state = random_state
        self.model.fit(self.x_scaled)
        self.labels= self.model.labels_
        sil_score = silhouette_score(self.x_scaled, self.labels)
        return (self.labels,sil_score)
    
def trai_kmeans_c_predictor(app) :
    from flasker.regressors.commonFunc import train_predictor
    return train_predictor(app,KMeansClustering,KMeans,5)

def train_kmeans_c_predictor_cust(app,req,test_size,random_state,cols1,cols2,cols3,eval_metric,n_clusters=5) :
    from flasker.regressors.commonFunc import train_predictor_cust
    return train_predictor_cust(app,KMeansClustering,KMeans,req,test_size,random_state,cols1,cols2,cols3,eval_metric,n_clusters)
