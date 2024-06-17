# CloudComputing

## Description

This is a REST API for WasiatD, a software that help people to detect their plant disease

## installation

1. Clone this Reposistory

```bash
git clone https://github.com/WasiatD/CloudComputing.git
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create `.firebaseconfig.py` using ur own key
4. Run the development program

```bash
python -u app.py
```

## Libraries Used

- [FastApi](https://fastapi.tiangolo.com) - FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.
- [pyrebase] - Pyrebase is a Python wrapper for the Firebase API, which simplifies the interaction with Firebase services such as Firebase Authentication, Firebase Realtime Database, Firebase Storage
- [Google Generative Ai](https://ai.google.dev/api/python/google/generativeai) - The Google AI Python SDK is the easiest way for Python developers to build with the Gemini API
- [Pillow](https://python-pillow.org/) - The Python Imaging Library adds image processing capabilities to your Python interpreter.
- [base64] - the base64 library offers functions for encoding and decoding binary data to and from base64 strings, effectively converting any binary data to plain text

## API Documentation

[API Documentation](https://documenter.getpostman.com/view/30684465/2sA3XMkPQr)

## GCP Deployment

This API is using Google Cloud Platform for deployment.

GCP Services used:

- Google Cloud Run
- Firebase Firestore

## Cloud Architecture

This is our project Cloud Architecture, illustrated using Visual Paradigm.

![Cloud Architecture](images\Capstone-Diagram-GCP.png)
