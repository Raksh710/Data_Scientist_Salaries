from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('rf2.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        work_year = int(request.form['work_year'])
        pay_grade=float(request.form['pay_grade'])
        company_country_pay_scale=int(request.form['company_country_pay_scale'])
        job_pay_scale = int(request.form['job_pay_scale'])
        experience_level = request.form['experience_level']
        if (experience_level == "EN"):
            experience_level_EN = 1
            experience_level_EX = 0
            experience_level_MI = 0
            experience_level_SE = 0
        elif (experience_level == "EX"):
            experience_level_EN = 0
            experience_level_EX = 1
            experience_level_MI = 0
            experience_level_SE = 0
        elif (experience_level == "MI"):
            experience_level_EN = 0
            experience_level_EX = 0
            experience_level_MI = 1
            experience_level_SE = 0
        elif (experience_level == "SE"):
            experience_level_EN = 0
            experience_level_EX = 0
            experience_level_MI = 0
            experience_level_SE = 1
        
        employment_type = request.form['employment_type']
        if (employment_type == "CT"):
            employment_type_CT = 1
            employment_type_FL = 0
            employment_type_FT = 0
            employment_type_PT = 0
        elif (employment_type == "FL"):
            employment_type_CT = 0
            employment_type_FL = 1
            employment_type_FT = 0
            employment_type_PT = 0
        elif (employment_type == "FT"):
            employment_type_CT = 0
            employment_type_FL = 0
            employment_type_FT = 1
            employment_type_PT = 0
        elif (employment_type == "PT"):
            employment_type_CT = 0
            employment_type_FL = 0
            employment_type_FT = 0
            employment_type_PT = 1
        
        remote_ratio = request.form['remote_ratio']
        if (remote_ratio=='Fully Remote'):
            remote_ratio_Full_Remote = 1
            remote_ratio_Hybrid = 0
            remote_ratio_On_prem = 0
        elif (remote_ratio=='Hybrid'):
            remote_ratio_Full_Remote = 0
            remote_ratio_Hybrid = 1
            remote_ratio_On_prem = 0
        elif (remote_ratio=='On-prem'):
            remote_ratio_Full_Remote = 0
            remote_ratio_Hybrid = 0
            remote_ratio_On_prem = 1
        
        company_size = request.form['company_size']
        if (company_size=='L'):
            company_size_L = 1
            company_size_M = 0
            company_size_S = 0
        elif (company_size=='M'):
            company_size_L = 0
            company_size_M = 1
            company_size_S = 0
        elif (company_size=='S'):
            company_size_L = 0
            company_size_M = 0
            company_size_S = 1
        
        pred = model.predict([[work_year, pay_grade, company_country_pay_scale, job_pay_scale,experience_level_EN, experience_level_EX, experience_level_MI,experience_level_SE, employment_type_CT, employment_type_FL,employment_type_FT, employment_type_PT,remote_ratio_Full_Remote,remote_ratio_Hybrid, remote_ratio_On_prem, 
                               company_size_L,company_size_M, company_size_S]])
        
        output=round(pred[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot get employed")
        else:
            return render_template('index.html',prediction_text="Your desired salary is: {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True,use_reloader=False)
