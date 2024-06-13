from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, FastAPI, Form
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from model import plant_disease_model
from auth import login_user, register_user, validate_token, get_current_user_id
from handler import add_prediction, get_predictions, getListIot, add_data,get_dataById
import base64   
import model
import tempfile
import shutil
import os
import jwt
import json
from datetime import datetime


app = FastAPI()

# Initialize the model with the path to the TFLite model file
model_path = "model_fix2"  # Replace with your model path
model = plant_disease_model(model_path=model_path)
class ImageData(BaseModel):
    base64_encoded: str

class User(BaseModel):
    email: str
    password: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Plant Disease Prediction API"}


@app.post("/addDataIOT")
async def add_data_iot(data: dict):
    try:
        timestamp = str(datetime.now().timestamp())
        email = data['email']
        add_data(email, data['id'], data, timestamp)
        return JSONResponse(content={"message": "Data added successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/register")
async def register(email: str = Form(...), password: str = Form(...)):
    try:
        user = register_user(email, password)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        error_detail = str(e)
        if hasattr(e, 'args') and len(e.args) > 1:
            try:
                error_detail = json.loads(e.args[1])
            except json.JSONDecodeError:
                error_detail = {"message": e.args[1]}
        else:
            error_detail = {"message": error_detail}
        
        raise HTTPException(status_code=400, detail=error_detail)

@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    try:
        # email = data['email']
        # password = data['password']
        token = login_user(email, password)
        return token
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Predict plant disease
@app.post("/predict")
async def predict_plant_disease(image_data: ImageData, token: str = Depends(oauth2_scheme)):
    try:
        # Validate the token
        validate_token(token)
        base64_encoded = image_data.base64_encoded
        predicted_class = model.predict_tf(base64_encoded)
        user = get_current_user_id(token)
        add_prediction(user,base64_encoded, predicted_class)

        return JSONResponse(content={"predicted_class": predicted_class})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# get disease info
@app.get("/disease-info/{disease}")
def get_disease_info(disease: str, token: str = Depends(oauth2_scheme)):
    try:
        validate_token(token)
        info = model.prompt_disease(disease)
        return JSONResponse(content={"disease_info": info})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# get List predictions
@app.get("/get_predictions")
def getpredictions(token: str = Depends(oauth2_scheme)):
    try:
        validate_token(token)
        user = get_current_user_id(token)
        print (user)
        predictions = get_predictions(user)
        return JSONResponse(content={"predictions": predictions})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# # get predictions by id 
# @app.get("/get_predictions/{id}")
# def get_prediction_by_id(id: str):
#     doc = model.db.collection('predictions').document(id).get()
#     return doc.to_dict()

# get list IOT
@app.get("/getListIot")
def get_list_iot(token: str = Depends(oauth2_scheme)):
    try:
        validate_token(token)
        user = get_current_user_id(token)
        isi = getListIot(user)
        return JSONResponse(content={"isi": isi})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# get data by id IOT
@app.get("/getDataById/{id}")
def get_data_by_id(id: str, token: str = Depends(oauth2_scheme)):
    try:
        validate_token(token)
        user = get_current_user_id(token)
        isi = get_dataById(user, id)
        return JSONResponse(content={"isi": isi})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)