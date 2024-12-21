from abc import ABC, abstractmethod
from sklearn.base import BaseEstimator
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from dataclasses import dataclass
from typing import Optional


@dataclass
class Prediction:
    outcome: float
    confidence: Optional[float] = None
    metric_name:Optional[str]=""
    y_pred:Optional[int]=None


class Predictor(ABC):
    def __init__(self, model: BaseEstimator, encoder: OneHotEncoder, metric, metric_name, cols1, cols2, cols3, req,categories=None,n_clusters=5) -> None:
        self.model = model
        self.metric = metric
        self.encoder = encoder
        self.metric_name = metric_name
        self.cols1 = cols1
        self.cols2 = cols2
        self.cols3 = cols3
        self.req = req
        self.categories=categories # dic de toutes les catégories pour les col dans cols1

    def predict(self, input) -> Prediction:
        df = pd.DataFrame([input])
        print(self.cols1,self.cols2)
        if len(self.cols1) >= 1:
            print('here')
            x1 = pd.DataFrame(self.encoder.transform(df[self.cols1]), columns=self.encoder.get_feature_names_out(self.cols1))
            x2 = df[self.cols2]
            x = pd.concat([x1, x2], axis=1)
        else:
            x = df[self.cols2]
        print("input",x)
        pred = self.model.predict(x)
        print(pred)
        if len(self.cols3) >= 1:
            return Prediction(outcome=pred, confidence=self.metric,metric_name=self.metric_name)
        else:
            return Prediction(outcome=pred, confidence=self.metric,metric_name=self.metric_name)


class InProgressPredictor(Predictor):
    @abstractmethod
    def predict_in_progress(self, input,scenario) -> Prediction:
        pass
