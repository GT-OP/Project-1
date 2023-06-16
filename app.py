# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 00:10:52 2022

@author: ASUS
"""
''' To run the program write python app.py in the terminal '''

from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
import new_one
app = Flask(__name__)
model = pickle.load(open('Copy_of_pr_cardekho_Copy1.pkl', 'rb'))
#,methods=['GET']
@app.route('/')
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        arr=new_one.arr1
        x=[]
        for i in range(0,133):
            x.append(0)
        
        Year = int(request.form['Year'])
        for i in range(0,133):
            if arr[i][1]==" no_years ":
                x[i]=Year

        Engine=int(request.form['engine'])
        ch=0
        for i in range(0,133):
            if arr[i]=="e":
                s=""
                for i in range(8,50):
                    if arr[i]==" ":
                        break
                    s=s+arr[i]

                if int(s)==Engine:
                    ch=1
                    x[i]=1
                    break
        if ch==0:
            Ind=-1
            maxe=10000000
            for i in range(0,133):
                if arr[i]=="e":
                    s=""
                    for i in range(8,50):
                        if arr[i]==" ":
                            break
                        s=s+arr[i]
                    r=int(s)
                    b=abs(Engine-r)    
                    if b<maxe:
                        ch=1
                        if ind!=-1:
                            x[ind]=0
                        x[i]=1
                        maxe=b
                        ind=i        
        
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        for i in range(0,133):
            if arr[i]==" km_driven ":
                x[i]=Kms_Driven2
        
        Owner=int(request.form['Owner'])
        for i in range(0,133):
            if arr[i]==" owner_Test Drive Car ":
                if Owner==1:
                    x[i]=1
            if arr[i]==" owner_Second Owner ":
                if Owner==2:
                    x[i]=1
            if arr[i]==" owner_Third Owner ":
                if Owner==3:
                    x[i]=1

        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0              
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        for i in range(0,133):
            if arr[i]==" fuel_Petrol ":
                x[i]=Fuel_Type_Petrol
            if arr[i]==" fuel_Diesel ":
                x[i]=Fuel_Type_Diesel

        
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0	
        for i in range(0,133):
            if arr[i]==" seller_type_Individual ":
                x[i]=Seller_Type_Individual


        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        for i in range(0,133):
            if arr[i]==" transmission_Manual ":
                x[i]=Transmission_Mannual

        prediction=model.predict([x])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_text="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)