import tensorflow as tf
from PIL import Image
import numpy as np
import google.generativeai as genai
import base64
import os
from io import BytesIO
from PIL import Image
import time
from config import GENAI_API_KEY

class plant_disease_model:
    def __init__(self, model_path):
        self.loaded_model = tf.saved_model.load(model_path)


    def predict_tf(self, base64_str, save_dir='saved_images'):
        class_names = [
            "Pepper__bell___Bacterial_spot", "Pepper__bell___healthy",
            "Strawberry___Leaf_scorch", "Strawberry___healthy",
            "Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_Late_blight",
            "Tomato_Leaf_Mold", "Tomato_Septoria_leaf_spot",
            "Tomato_Spider_mites_Two_spotted_spider_mite", "Tomato__Target_Spot",
            "Tomato__Tomato_YellowLeaf__Curl_Virus", "Tomato__Tomato_mosaic_virus",
            "Tomato_healthy"
        ]

        # Decode the base64 string to get image data
        img_data = base64.b64decode(base64_str)
        img = Image.open(BytesIO(img_data))

        # Preprocess the image
        img_resize = img.resize((299, 299))  # Resize the image to match model input size
        img_array = np.array(img_resize)  # Convert image to numpy array
        img_array = img_array.astype(np.float32) / 255.0  # Normalize pixel values and convert to float32

        # Predict the class of the image using the loaded_model directly
        prediction = self.loaded_model(np.expand_dims(img_array, axis=0))

        # Get the predicted class index
        predicted_class_index = np.argmax(prediction)
        
        # Get the predicted class name
        predicted_class_name = class_names[predicted_class_index]

        ###### SIMPAN DECODED BASE64 IMAGE
        # Ensure the save directory exists
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Generate a unique filename using the predicted class name and a timestamp
        timestamp = int(time.time())
        image_name = f"{predicted_class_name}_{timestamp}.jpg"
        save_path = os.path.join(save_dir, image_name)

        # Save the image to the specified directory
        img.save(save_path)
        return predicted_class_name

    def prompt_disease(self, disease):
        genai.configure(api_key=GENAI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Jelaskan Penyakit {disease}: Pengertian, Penyebab, dan Cara Penanganan singkat dalam 3 paragraf."
        response = model.generate_content(prompt)
        return response.text

    def main_tf(self, image_path):
        # Load the image and predict the class
        predicted_class_name = self.predict_tf(image_path)

        # Print the predicted class name
        print(self.prompt_disease(predicted_class_name))
