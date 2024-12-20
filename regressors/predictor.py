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


class Predictor(ABC):
    def __init__(self, model: BaseEstimator, encoder: OneHotEncoder, metric, metric_name, cols1, cols2, cols3, req) -> None:
        self.model = model
        self.metric = metric
        self.encoder = encoder
        self.metric_name = metric_name
        self.cols1 = cols1
        self.cols2 = cols2
        self.cols3 = cols3
        self.req = req

    def predict(self, input) -> Prediction:
        df = pd.DataFrame([input])
        if len(self.cols1) > 1 and len(self.cols3) > 0:
            x1 = pd.DataFrame(self.encoder.transform(df[self.cols1]), columns=self.encoder.get_feature_names_out(self.cols1))
            x2 = df[self.cols2]
            x = pd.concat([x1, x2], axis=1)
            pred = self.model.predict(x)
            return Prediction(outcome=pred, confidence=self.metric,metric_name=self.metric_name)
        elif len(self.cols3) > 0:
            x = df[self.cols2]
            pred = self.model.predict(x)
            return Prediction(outcome=pred, confidence=self.metric,metric_name=self.metric_name)
        else:
            raise ValueError("La structure n'est pas valide pour la prévision.")


class InProgressPredictor(Predictor):
    @abstractmethod
    def predict_in_progress(self, input,scenario) -> Prediction:
        pass
