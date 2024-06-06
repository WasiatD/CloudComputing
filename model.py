import numpy as np
import tensorflow as tf
import google.generativeai as genai
import base64
import io
from PIL import Image
import os
import firebase_admin
from firebase_admin import credentials, firestore
from config import GENAI_API_KEY

class PlantDiseaseModel:
    def __init__(self, model_path: str, firestore_db):
        self.model_path = model_path
        self.class_names = [
            "Pepper_bell_Bacterial_spot", "Pepper_bell_healthy",
            "Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_Late_blight",
            "Tomato_Leaf_Mold", "Tomato_Septoria_leaf_spot",
            "Tomato_Spider_mites_Two_spotted_spider_mite", "Tomato_Target_Spot",
            "Tomato_YellowLeaf_Curl_Virus", "Tomato_Tomato_mosaic_virus",
            "Tomato_healthy"
        ]
        self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()
        self.save_dir = "saved_images"
        os.makedirs(self.save_dir, exist_ok=True)
        self.db = firestore_db

    def predict_image_from_base64(self, base64_str: str) -> str:
        # Decode the base64 string to bytes
        image_data = base64.b64decode(base64_str)
        
        # Convert bytes to a PIL Image
        image = Image.open(io.BytesIO(image_data))
        
        # Save the image to the server
        image_path = os.path.join(self.save_dir, "uploaded_image.jpg")
        image.save(image_path)

        # Resize the image to match the expected dimensions
        image = image.resize((299, 299))
        
        # Perform prediction as before
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.expand_dims(input_arr, axis=0)
        input_arr = input_arr / 255.0  # Normalize the input image

        input_index = self.interpreter.get_input_details()[0]['index']
        self.interpreter.set_tensor(input_index, input_arr)
        self.interpreter.invoke()

        output_index = self.interpreter.get_output_details()[0]['index']
        output = self.interpreter.get_tensor(output_index)
        predicted_class_index = np.argmax(output)
        predicted_class_name = self.class_names[predicted_class_index]

        try:
            doc_ref = self.db.collection('predictions').add({
                'image': base64_str,
                'predicted_class': predicted_class_name
            })
            print(f'Document added with ID: {doc_ref[1].id}')
        except Exception as e:
            print(f'Error adding document to Firestore: {e}')

        return predicted_class_name

def prompt_disease(disease: str) -> str:
    genai.configure(api_key=GENAI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Jelaskan Penyakit {disease}: Pengertian, Penyebab, dan Cara Penanganan singkat dalam 3 paragraf."
    response = model.generate_content(prompt)
    return response.text

service_account_key_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', './belajar-firestore-7ddb4-firebase-adminsdk-jr4kg-1cb628449b.json')
cred = credentials.Certificate(service_account_key_path)
firebase_admin.initialize_app(cred)
db = firestore.client()