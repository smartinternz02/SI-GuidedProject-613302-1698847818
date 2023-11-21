# save this as app.py
from flask import Flask, request, render_template
import pickle
import numpy as np
from markupsafe import escape

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
scale = pickle.load(open('scale.pkl','rb'))

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method ==  'POST':
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        credit = float(request.form['credit'])
        proparea = request.form['proparea']
        ApplicantIncome=float(request.form['ApplicantIncome'])
        CoapplicantIncome=float(request.form['CoapplicantIncome'])
        LoanAmount=float(request.form['LoanAmount'])
        Loan_Amount_Term=float(request.form['loan_Amount_Term'])
        
        # gender
        if (gender == "Male"):
            male=1
        else:
            male=0
        
        
        # married
        if(married=="Yes"):
            married_yes = 1
        else:
            married_yes=0

        # dependents
        if(dependents=='3+'):
            dependents = 3

        # education
        if (education=="Not Graduate"):
            not_graduate=1
        else:
            not_graduate=0

        # employed
        if (employed == "Yes"):
            employed_yes=1
        else:
            employed_yes=0

        # property area

        if proparea == 'Urban':
            proparea = 2
        elif proparea == 'Rural':
            proparea = 0
        else:
            proparea = 1  

        features = [credit, male, married_yes, dependents, not_graduate, employed_yes, proparea, ApplicantIncome, CoapplicantIncome,LoanAmount,Loan_Amount_Term ]
        con_features = [np.array(features)]
        scale_features = scale.fit_transform(con_features)
        prediction = model.predict(scale_features)
    
        # print(prediction)
        print(prediction)
        if prediction==0:
            return render_template('approve.html',prediction_text ='Congratulations! You are eligible for loan')
        else:
            return render_template('reject.html',prediction_text ='Sorry You are not eligible for loan')
    else:
        return render_template("prediction.html")
if __name__ == "__main__":
    app.run(debug=True)