from flask import Blueprint, request, jsonify, current_app
from flasker.app import db
from flasker.models import Users
from flasker.forms import UserForm,LoginForm
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,login_user,current_user,logout_user
from werkzeug.utils import secure_filename
import uuid as uuid
import os

# Create a Blueprint for user routes
api_bp = Blueprint('api', __name__)


@api_bp.route('/dtpredict', methods=['POST'])
def dtpredict():
    dt_predictor = current_app.dt_predictor
    input_data = request.json.get('input_data', [])
    if not input_data:
        return jsonify({"erreur": "Pas de données fournies"}), 400
    try:
        prediction = dt_predictor.predict(input_data)
        print(prediction)
        return jsonify({"prediction":   {
                "outcome": prediction.outcome.tolist()[0],
                "confidence": prediction.confidence,
                "metric_name":prediction.metric_name
            }}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@api_bp.route('/trainkmeanclustering', methods=['POST'])   
def kmeans():
    kmc=current_app.kmc_predictor
    n= request.json.get('n')
    rs=request.json.get('rs')
    if n is None or rs is None:
            return jsonify({"error": "Pas de données fournies"}), 400
    res=kmc.train(n,rs)
    print(res)
    return jsonify({"n": n, "rs": rs, "message": "Successfully processed"}), 200
