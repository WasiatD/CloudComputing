# app.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from model import PlantDiseaseModel, prompt_disease
import model
import tempfile
import shutil
import os
import base64   

app = FastAPI()

# Initialize the model with the path to the TFLite model file
model_path = "plant_model.tflite"  # Replace with your model path
model = PlantDiseaseModel(model_path=model_path, firestore_db=model.db)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Plant Disease Prediction API"}

@app.post("/predict")
async def predict_plant_disease(base64_encoded: str):
    try:
        # Make a prediction using the base64 encoded image data
        predicted_class = model.predict_image_from_base64(base64_encoded)
        
        return JSONResponse(content={"predicted_class": predicted_class})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/disease-info/{disease}")
def get_disease_info(disease: str):
    try:
        info = prompt_disease(disease)
        return JSONResponse(content={"disease_info": info})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get_predictions")
def get_predictions():
    predictions = []
    docs = model.db.collection('predictions').stream()
    for doc in docs:
        predictions.append(doc.to_dict())
    return {"predictions": predictions}

# get predictions by id 
@app.get("/get_predictions/{id}")
def get_prediction_by_id(id: str):
    doc = model.db.collection('predictions').document(id).get()
    return doc.to_dict()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# http://127.0.0.1:8000/docs