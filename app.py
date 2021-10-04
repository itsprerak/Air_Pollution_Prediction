from flask import Flask, request,render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

app = Flask(__name__,template_folder='Templates')
model = pickle.load(open("aqi_extr.pkl", "rb"))


# @app.route("/")
# @cross_origin()
# def home():
#     return render_template("review-page.html")



@app.route("/", methods = ["GET", "POST"])
@cross_origin()
def predict():
    prediction_text = "dummy dum dum"
    if request.method == "POST":

        # Date_of_Journey
        PM2 = request.form["PM2"]
        PM10 = request.form["PM10"]
        CO = request.form["CO"]
        NO = request.form["NO"]
        NO2 = request.form["NO2"]
        NOx = request.form["NOx"]
        Ozone = request.form["Ozone"]
        SO2 = request.form["SO2"]
        Benzene = request.form["Benzene"]
        Toluene = request.form["Toluene"]
        Ammonia = request.form["Ammonia"]
        Year = request.form["Year"]
        Month = request.form["Month"]
        City = request.form["City"]
        
        if(City=="Aizawl" or City=="Shillong" or City=="Coimbatore" or City=="Thiruvananthapuram" or City=="Ernakulam" or City=="Amaravati" or City=="Bengaluru" or City=="Chandigarh" or City=="Kochi"):
            City_Group_B = 0
            City_Group_C = 0
            City_Group_D = 0
            City_Group_E = 0
            City_Group_F = 0

        elif(City=="Mumbai" or City=="Hyderabad" or City=="Chennai" or City=="Visakhapatnam" or City=="Amritsar" or City=="Bhopal" or City=="Jaipur" or City=="Guwahati" or City=="Kolkata" or City=="Jorapokhar" or City=="Brajrajnagar"):
            City_Group_B = 1
            City_Group_C = 0
            City_Group_D = 0
            City_Group_E = 0
            City_Group_F = 0
        
        elif(City=="Talcher" or City=="Lucknow" or City=="Gurugram" or City=="Patna"):
            City_Group_B = 0
            City_Group_C = 1
            City_Group_D = 0
            City_Group_E = 0
            City_Group_F = 0

        elif(City=="Delhi"):
            City_Group_B = 0
            City_Group_C = 0
            City_Group_D = 1
            City_Group_E = 0
            City_Group_F = 0

        elif(City=="Ahmedabad"):
            City_Group_B = 0
            City_Group_C = 0
            City_Group_D = 0
            City_Group_E = 0
            City_Group_F = 1

        if(Month=="January"):
            m=1
        elif(Month=="February"):
            m=2
        elif(Month=="March"):
            m=3
        elif(Month=="April"):
            m=4
        elif(Month=="May"):
            m=5
        elif(Month=="June"):
            m=6
        elif(Month=="July"):
            m=7
        elif(Month=="August"):
            m=8
        elif(Month=="September"):
            m=9
        elif(Month=="October"):
            m=10
        elif(Month=="November"):
            m=11
        else:
            m=12

        X = pd.DataFrame([
            PM2,
            PM10,
            NO,
            NO2,
            NOx,
            Ammonia,
            CO,
            SO2,
            Ozone,
            Benzene,
            Toluene,
            Year,
            m,
            City_Group_B,
            City_Group_C,
            City_Group_D,
            City_Group_E,
            City_Group_F
        ])
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        scaler.fit(X)
        X = scaler.transform(X)

        prediction=model.predict(X)

        output=round(prediction[0],2)
        if(output<=50):
            air_qual = "GOOD"
        elif(output<=100):
            air_qual="SATISFACTORY"
        elif(output<=200):
            air_qual="MODERATE"
        elif(output<=300):
            air_qual="POOR"
        elif(output<=400):
            air_qual="VERY POOR"
        else:
            air_qual="SEVERE"

        prediction_text = "AQI : {} - {}".format(output, air_qual)
        # We throw this string onto the html in the form of a variable i.e prediction_text
        # there with Jinja Templating you can pay around with it
        
        return render_template("result.html", prediction_text = prediction_text)

    return render_template("review-page.html")


if __name__ == "__main__":
    app.run(debug=True)