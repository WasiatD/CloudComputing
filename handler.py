from firebaseconfig import db


def add_data(user, data):
    try:
        db.collection('user').document(user).collection('IOT').document(data['id']).set({'id': data['id'], 'name':data['name'], 'location':data['location'], 'suhu':data['suhu'],'ph':data['ph'], 'kelembapan':data['kelembaban']})
    except Exception as e:
        raise e

def add_prediction(user ,base64_str, predicted_class_name):
    try:
        db.collection('user').document(user).collection('prediction').add({
                'image': base64_str,
                'predicted_class': predicted_class_name
            })
    except Exception as e:
        raise e

def get_predictions(user):
    try:
        predictions = []
        docs = db.collection('user').document(user).collection('prediction').stream()
        for doc in docs:
            predictions.append(doc.to_dict())
        return predictions
    except Exception as e:
        raise e

def getListIot(user):
    try:
        collection_ref = db.collection('user').document(user).collection('IOT')
        docs = collection_ref.stream()
        isi = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data['id'] = doc.id
            isi.append(doc_data)

        return isi
    except Exception as e:
        raise e

def get_dataById(user, id):
    try:
        doc = db.collection('user').document(user).collection('IOT').document(id)
        doc = doc.get()
        return doc.to_dict()
    except Exception as e:
        raise e

