# app.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from model import plant_disease_model
import model
import tempfile
import shutil
import os
import base64   
from datetime import datetime

app = FastAPI()

# Initialize the model with the path to the TFLite model file
model_path = "model_fix2"  # Replace with your model path
model = plant_disease_model(model_path=model_path,firestore_db=model.db)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Plant Disease Prediction API"}


@app.post("/addDataIOT")
async def add_data_iot(data: dict):
    try:
        timestamp = str(datetime.now().timestamp())
        doc_ref = model.db.collection('user').document('user').collection('IOT').document('iot1').collection('data').document(timestamp).set(data)
        return JSONResponse(content={"message": "Data added successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict")
async def predict_plant_disease(base64_encoded: str):
    try:
        # Make a prediction using the base64 encoded image data
        predicted_class = model.predict_tf(base64_encoded)
        
        return JSONResponse(content={"predicted_class": predicted_class})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/disease-info/{disease}")
def get_disease_info(disease: str):
    try:
        info = model.prompt_disease(disease)
        return JSONResponse(content={"disease_info": info})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/get_predictions")
def get_predictions():
    predictions = []
    docs = model.db.collection('user').document('user').collection('prediction').stream()
    for doc in docs:
        predictions.append(doc.to_dict())
    return {"predictions": predictions}

# get predictions by id 
@app.get("/get_predictions/{id}")
def get_prediction_by_id(id: str):
    doc = model.db.collection('user').document('user').collection('prediction').document(id).get()
    return doc.to_dict()

@app.get("/getListIot")
def get_list_iot():
    try:
        collection_ref = model.db.collection('user').document('user').collection('IOT')
        docs = collection_ref.stream()
        isi = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data['id'] = doc.id
            isi.append(doc_data)

        return JSONResponse(content={"isi": isi})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/getDataById/{id}")
def get_data_by_id(id: str):
    try:
        doc = model.db.collection('user').document('user').collection('IOT').document(id).collection('data')
        docs = doc.stream()
        isi = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data['id'] = doc.id
            isi.append(doc_data)

        return JSONResponse(content={"isi": isi})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

# http://localhost:8000/docs