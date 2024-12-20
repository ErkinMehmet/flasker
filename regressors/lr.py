from typing import List
from sklearn.linear_model import LinearRegression
from flasker.regressors.predictor import Predictor
from flasker.regressors.commonFunc import train_predictor

class LinearRegressionPredictor(Predictor):
    def __init__(self, model: LinearRegression, encoder, metric, 
                 metric_name: str, cols1: List[str], cols2: List[str], cols3: List[str], req) -> None:
        super().__init__(model, encoder, metric, metric_name, cols1, cols2, cols3, req)

def train_linear_regression_predictor(app):
    return train_predictor(app, LinearRegressionPredictor, LinearRegression)
