import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

X = ['Tenure', 'WarehouseToHome', 'NumberOfDeviceRegistered',
       'NumberOfAddress', 'DaySinceLastOrder', 'CashbackAmount',
       'PreferredLoginDevice_Computer', 'PreferredLoginDevice_Mobile',
       'CityTier_1', 'CityTier_2', 'CityTier_3', 'PreferredPaymentMode_CC',
       'PreferredPaymentMode_COD', 'PreferredPaymentMode_DC',
       'PreferredPaymentMode_E wallet', 'PreferredPaymentMode_UPI',
       'PreferedOrderCat_Fashion', 'PreferedOrderCat_Grocery',
       'PreferedOrderCat_Laptop', 'PreferedOrderCat_Mobile',
       'PreferedOrderCat_Others', 'SatisfactionScore_1', 'SatisfactionScore_2',
       'SatisfactionScore_3', 'SatisfactionScore_4', 'SatisfactionScore_5',
       'MaritalStatus_Divorced', 'MaritalStatus_Married',
       'MaritalStatus_Single', 'Gender_Female', 'Gender_Male', 'Complain_0',
       'Complain_1']
len(X)

def predict_price(tenure, warehouse, numdevice, numaddress, lastorder, cashback, logindevice, citytier, paymentmode, ordercat, score, maritalstatus, gender, complain):    
    logindevice_index = X.index('PreferredLoginDevice_' + logindevice)
    citytier_index = X.index('CityTier_' + citytier)
    paymentmode_index = X.index('PreferredPaymentMode_' + paymentmode)
    ordercat_index = X.index('PreferedOrderCat_' + ordercat)
    score_index = X.index('SatisfactionScore_' + score)
    maritalstatus_index = X.index('MaritalStatus_' + maritalstatus)
    gender_index = X.index('Gender_' + gender)
    complain_index = X.index('Complain_' + complain)

    index_list = [logindevice_index, citytier_index, paymentmode_index, ordercat_index, score_index, maritalstatus_index, gender_index, complain_index]

    x = np.zeros(len(X))
    x[0] = tenure
    x[1] = warehouse
    x[2] = numdevice
    x[3] = numaddress
    x[4] = lastorder
    x[5] = cashback

    for ind in index_list:
      if ind >= 0:
          x[ind] = 1

    #for media in media_type_list:
    #  media_index = X.columns.get_loc('media_type_' + media)
    #  if media_index >= 0:
    #    x[media_index] = 1

    return model.predict([x])[0]


app = Flask(__name__)

model = pickle.load(open('churn.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    if request.method == 'POST':
        tenure = float(request.form['tenure'])
        warehouse = float(request.form['warehousetohome'])
        numdevice = float(request.form['numdevices'])
        numaddress = float(request.form['numaddress'])
        lastorder = float(request.form['lastorder'])
        cashback = float(request.form['cashbackamount'])
        logindevice = request.form['logindevice']
        citytier = request.form['citytier']
        paymentmode = request.form['paymentmode']
        ordercat = request.form['ordercat']
        score = request.form['satisfactionscore']
        maritalstatus =request.form['maritalstatus']
        gender = request.form['gender']
        complain = request.form['complain']
  

    prediction = predict_price(tenure, warehouse, numdevice, numaddress, lastorder, cashback, logindevice, citytier, paymentmode, ordercat, score, maritalstatus, gender, complain)    
  
    return render_template('index.html', prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)