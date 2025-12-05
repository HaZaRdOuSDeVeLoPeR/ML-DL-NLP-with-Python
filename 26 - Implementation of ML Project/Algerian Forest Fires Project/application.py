import pickle
import pandas as pd
import numpy as np
from flask import *
from sklearn.preprocessing import StandardScaler

# create flask app instance
application = Flask(__name__, template_folder = 'templates', static_folder = 'static')

# import all models and the scaler
scaler = pickle.load(open('./models/scaler.pkl', 'rb'))
ridge = pickle.load(open('./models/ridge.pkl', 'rb'))
lasso = pickle.load(open('./models/lasso.pkl', 'rb'))
elasticnet = pickle.load(open('./models/elasticnet.pkl', 'rb'))

@application.route('/', methods = ['GET'])
def welcome():
    return render_template('homepage.html')

@application.route('/predictform', methods = ['GET'])
def query_parameters():
    return render_template('userinput.html')

@application.route('/predictdata', methods = ['POST'])
def predict_result():
    model = request.form.get('Model', None)
    col_names = ['Temperature', 'RH', 'WS', 'Rain', 'FFMC', 'DMC', 'DC', 'ISI', 'BUI']

    input = pd.DataFrame([[request.form.get(x) for x in col_names]], columns = col_names)
    input = pd.DataFrame(scaler.transform(input), columns = ['Temperature', 'RH', 'WS', 'Rain', 'FFMC', 'DMC', 'DC', 'ISI', 'BUI'])

    fwi = 0.0
    if model == 'ridge':
        fwi = ridge.predict(input)[0]
    elif model == 'lasso':
        fwi = lasso.predict(input)[0]
    else:
        fwi = elasticnet.predict(input)[0]

    fwi = f'FWI = {fwi}'
    return render_template('userinput.html', result = fwi)

if __name__ == '__main__':
    application.run(host = '0.0.0.0', port = 8080, debug = True)